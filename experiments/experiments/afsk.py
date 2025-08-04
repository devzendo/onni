from abc import ABC, abstractmethod
from typing import List
import math

class PacketObserver(ABC):
    @abstractmethod
    def notify(self, packet):
        pass

class AfskCorrelator:
    def __init__(self, sample_rate,  *observers: List[PacketObserver]):
        self.sample_rate = sample_rate
        self.observers = observers
        print(f"observers are {self.observers}")

        # Peak abs value
        self.peak = 0.0
        self.decay = 1.0 -  math.exp(math.log(0,5) / float(sample_rate))
        print(f"decay {self.decay}")

    def notify_packet(self, packet):
        for obs in self.observers:
            obs.notify(packet)

    def process_sample(self, sample):
        print("sample: %s" % (hex(sample[0])))
        abs_sample = abs(sample)
        if abs_sample > self.peak:
            self.peak = abs_sample
        else:
            self.peak -= (self.peak * self.decay)
        pass