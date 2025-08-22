from abc import ABC, abstractmethod
from array import array
from enum import Enum
from pprint import pprint
from typing import List
import math

from experiments.filters import sample_rates, time_domain_filter_full, corr_diff_filter
from experiments.packet import Packet

class PacketObserver(ABC):
    @abstractmethod
    def notify(self, packet):
        pass

class State(Enum):
    WAITING = 1
    JUST_SEEN_FLAG = 2
    DECODING = 3


def java_round(x):
    return math.floor(x + 0.5)

class AfskCorrelator:
    def __init__(self, sample_rate,  *observers: List[PacketObserver]):
        self.sample_rate = sample_rate
        self.observers = observers
        print(f"observers are {self.observers}")

        # Peak abs value
        self.peak = 0.0
        self.decay = 1.0 -  math.exp(math.log(0.5) / float(sample_rate))
        print(f"decay {self.decay}")

        for rate_index in range(len(sample_rates)):
            if sample_rates[rate_index] == sample_rate:
                break
        if rate_index == len(sample_rates):
            raise ValueError(f"Sample rate {sample_rate} not supported")

        self.samples_per_bit = sample_rate / 1200.0
        print("samples_per_bit = %.3f" % self.samples_per_bit)
        # Not yet supporting the switchable 0 / 6dB emphasis change
        tdf = time_domain_filter_full
        filter_length = 32 # ???
        for filter_index in range(len(tdf)):
            print("Available filter length %d" % len(tdf[filter_index][rate_index]))
            if filter_length == len(tdf[filter_index][rate_index]):
                  print(f"Using filter length {filter_length}")
                  break
        if filter_index == len(tdf):
            filter_index = len(tdf) - 1
            print("Filter length %d not supported; using length %d" % (filter_length, len(tdf[filter_index][rate_index])))
		
        self.td_filter = tdf[filter_index][rate_index]
        self.cd_filter = corr_diff_filter[filter_index][rate_index]

        print("filter lengths are %d and %d" % (len(self.td_filter),len(self.cd_filter)))

        self.x = array('f', [0.0]) * len(self.td_filter)
        self.u1  = array('f', [0.0]) * len(self.td_filter)

        spb = math.floor(self.samples_per_bit)
        # Might it be better to use python's usual complex type here?
        self.c0_real = array('f', [0.0]) * spb
        self.c0_imag = array('f', [0.0]) * spb
        self.c1_real = array('f', [0.0]) * spb
        self.c1_imag = array('f', [0.0]) * spb

        self.diff = array('f', [0.0]) * len(self.cd_filter)
        self.previous_fdiff = 0.0

        self.last_transition = 0
        self.t = 0 # // running sample counter

        # Phase increments for the two frequencies used, 1200 and 2200Hz.
        self.phase_inc_f0 = (2.0 * math.pi * 1200.0 / sample_rate)
        self.phase_inc_f1 = (2.0 * math.pi * 2200.0 / sample_rate)
        self.phase_inc_symbol = (2.0 * math.pi * 1200.0 / sample_rate)

        self.j_td = 0 # time domain index
        self.j_cd = 0 # time domain index
        self.j_corr = 0 # correlation index

        self.phase_f0 = 0.0
        self.phase_f1 = 0.0

        # Diagnostic variables for estimating packet quality

        self.f0_period_count = int(0)
        self.f1_period_count = int(0)
        self.f0_max = float(0.0)
        self.f1_min = float(0.0) # to collect average max, min in the filtered diff signal
        self.f0_current_max = float(0.0)
        self.f1_current_min = float(0.0)
        self.max_period_error = float(0.0)

        self.state = State.WAITING
        self.data_carrier = False
        self.flag_count = int(0)
        self.flag_separator_seen = False
        self.decode_count = int(0)
        self.data = int(0)
        self.bitcount = int(0)

        self.packet = None

        #print(f"the correlator is {pprint(vars(self))}")


    def statistics_init(self):
        self.f0_period_count = int(0)
        self.f1_period_count = int(0)
        self.f0_max = float(0.0)
        self.f1_min = float(0.0)
        self.max_period_error = float(0.0)

    def statistics_finalize(self):
        self.f0_max = self.f0_max / self.f0_period_count
        self.f1_min = self.f1_min / self.f1_period_count

    def notify_packet(self, packet):
        for obs in self.observers:
            obs.notify(packet)

    def process_sample(self, sample):
        assert len(sample) == 1
        sample_0 = sample[0]
        #print("sample: %s" % (hex(sample_0)))
        
        abs_sample = abs(sample_0)
        if abs_sample > self.peak:
            self.peak = abs_sample
        else:
            self.peak -= (self.peak * self.decay)
        
        self.u1[self.j_td] = sample_0
        self.x[self.j_td]  = filter(self.u1, self.j_td, self.td_filter)
        
        self.c0_real[self.j_corr] = self.x[self.j_td] * math.cos(self.phase_f0)
        self.c0_imag[self.j_corr] = self.x[self.j_td] * math.sin(self.phase_f0)
			
        self.c1_real[self.j_corr] = self.x[self.j_td] * math.cos(self.phase_f1)
        self.c1_imag[self.j_corr] = self.x[self.j_td] * math.sin(self.phase_f1)

        self.phase_f0 += self.phase_inc_f0
        if (self.phase_f0 > 2.0 * math.pi):
            self.phase_f0 -= 2.0 * math.pi
        self.phase_f1 += self.phase_inc_f1
        if (self.phase_f1 > 2.0 * math.pi):
            self.phase_f1 -= 2.0 * math.pi

        cr = sum(self.c0_real, self.j_corr)
        ci = sum(self.c0_imag, self.j_corr)
        c0 = math.sqrt(cr*cr + ci*ci)

        cr = sum(self.c1_real, self.j_corr)
        ci = sum(self.c1_imag, self.j_corr)
        c1 = math.sqrt(cr*cr + ci*ci)

        self.diff[self.j_cd] = c0 - c1
        fdiff = filter(self.diff, self.j_cd, self.cd_filter)

        if (self.previous_fdiff * fdiff < 0.0 or self.previous_fdiff == 0.0):
            # we found a transition
            p = self.t - self.last_transition
            self.last_transition = self.t

            bits = int(java_round(float(p) / self.samples_per_bit))
            print("$ %f %d" % (float(p) / self.samples_per_bit, bits))

            # collect statistics
            if (fdiff < 0): # last period was high, meaning f0
                self.f0_period_count += 1
                self.f0_max += self.f0_current_max
                err = float(abs(bits - (float(p) / self.samples_per_bit)))
                print(")) %.02f %d %.02f\n" % (float(p) / self.samples_per_bit, bits, err))
                if (err > self.max_period_error):
                    self.max_period_error = err

                # prepare for the period just starting now
                self.f1_current_min = fdiff
            else:
                self.f1_period_count += 1
                self.f1_min += self.f1_current_min
                err = float(abs(bits - (float(p) / self.samples_per_bit)))
                print(")) %.02f %d %.02f\n" % (float(p) / self.samples_per_bit, bits, err))
                if (err > self.max_period_error):
                    self.max_period_error = err

                # prepare for the period just starting now
                self.f0_current_max = fdiff

            if (bits == 0 or bits > 7):
                self.state = State.WAITING
                self.data_carrier = False
                self.flag_count = 0
            else:
                if bits == 7:
                    self.flag_count += 1
                    self.flag_separator_seen = False
                    print("Seen %d flags in a row\n" % self.flag_count)

                    self.data = 0
                    self.bitcount = 0
                    match self.state:
                        case State.WAITING:
                            self.state = State.JUST_SEEN_FLAG
                            self.data_carrier = True

                            self.statistics_init()  # start measuring a new packet

                        case State.JUST_SEEN_FLAG:
                            pass

                        case State.DECODING:
                            if (self.packet is not None and self.packet.terminate()):
                                self.statistics_finalize()
                                # packet.statistics(new float[] { emphasis, f0_max / -f1_min, max_period_error });
                                print("%.02f:%.02f\n" % (self.f0_max / -self.f1_min, self.max_period_error))
                                self.decode_count += 1
                                print(f"decode count: {self.decode_count}: {self.packet}")
                                self.notify_packet(self.packet.bytes_without_crc())
                            self.packet = None
                            self.state = State.JUST_SEEN_FLAG
                else: # bits == 7
                    match self.state:
                        case State.WAITING:
                            pass
                        case State.JUST_SEEN_FLAG:
                            self.state = State.DECODING
                        case DECODING:
                            pass
                    if self.state == State.DECODING:
                        if bits != 1:
                            self.flag_count = 0
                        else:
                            if self.flag_count > 0 and not self.flag_separator_seen:
                                self.flag_separator_seen = True
                            else:
                                self.flag_count = 0

                        for k in range(bits - 1):
                            self.bitcount += 1
                            self.data >>= 1
                            self.data += 128
                            if self.bitcount == 8:
                                if self.packet is None:
                                    self.packet = Packet()
                                # if (data==0xAA) packet.terminate();
                                if not self.packet.add_byte(self.data):
                                    self.state = State.WAITING
                                    self.data_carrier = False
                                # System.out.printf(">>> %02x %c %c\n", data, (char)data, (char)(data>>1));
                                self.data = 0
                                self.bitcount = 0
                        if bits - 1 != 5: # the zero after the ones is not a stuffing
                            self.bitcount += 1
                            self.data >>= 1
                            if self.bitcount == 8:
                                if self.packet is None:
                                    self.packet = Packet()
                                # if (data==0xAA) packet.terminate();
                                if not self.packet.add_byte(self.data):
                                    self.state = State.WAITING
                                    self.data_carrier = False
                                # System.out.printf(">>> %02x %c %c\n", data, (char)data, (char)(data>>1));
                                self.data = 0
                                self.bitcount = 0
        # if previous_fdiff * fdiff < 0 or previous_fdiff == 0
        self.previous_fdiff = fdiff
        self.t += 1

        self.j_td += 1
        if self.j_td == len(self.td_filter):
            self.j_td = 0
        
        self.j_cd += 1
        if self.j_cd == len(self.cd_filter):
            self.j_cd = 0

        self.j_corr += 1
        if self.j_corr == len(self.c0_real): # samples_per_bit
            self.j_corr = 0

        






# Filter a signal x stored in a cyclic buffer with a FIR filter f
# The length of x must be larger than the length of the filter.
def filter(x: List[float], j: int, f: List[float]):
    c = 0.0
    for i in range(len(f)):
        c += x[j] * f[i]
        j -= 1
        if (j == -1):
            j = len(x) - 1
    return c

def sum(x: List[float], j: int):
    c = 0.0
    for i in range(len(x)):
        c += x[j]
        j -= 1
        if (j == -1):
            j = len(x) - 1
    return c

