import array
import pytest
import wave
from experiments.afsk import AfskCorrelator, PacketObserver

wav_filename = "../samples/4Z1PF_3_MAXTRAC-mono-shortened.wav"
#wav_filename = "../samples/01_40-Mins-Traffic-on-144.39.wav"

class WavReader:
    def __init__(self, filename):
        self.wav_file = wave.open(filename, 'rb')
        self.count = -1
        print(f"there are {self.wav_file.getnframes()} frames at {self.wav_file.getframerate()} Hz")

    def __enter__(self):
        return self

    def __exit__(self, value, traceback, wotevs):
        print("closing wav")
        self.wav_file.close()

    def __iter__(self):
        return self
    def __next__(self): 
        #if self.count == 80000:
        #    print("exhausted")
        #    raise StopIteration
        self.count += 1
        try:
            samples: bytes = self.wav_file.readframes(1)
            if len(samples) == 0:
                print("Read empty frame; exhausted")
                raise StopIteration

            #print(f"frame {self.count}: the read frame is {len(samples)} bytes long")
            pcm_samples = array.array("h", samples)
            return pcm_samples
        except BaseException as error:
            print(f"Error reading from waveform: {error}")
            raise StopIteration


class Counter(PacketObserver):
    def __init__(self):
        self.count = 0
        
    def notify(self, packet):
        print(f"got a packet {packet}")
        self.count+=1
        
def test_counter_observer():
    counter = Counter()
    assert counter.count == 0
    sample_rate = 44100
    afsk = AfskCorrelator(sample_rate, (counter))
    afsk.notify_packet("imagine a packet")
    assert counter.count == 1

def test_wavreader_open():
    try:
        wr = WavReader(wav_filename)
    except BaseException as e:
        print(f"Exception on construction: {e}")
        assert False, f"Exception on construction: {e}"
    
def test_processing_waveform():
    counter = Counter()
    sample_rate = 44100
    afsk = AfskCorrelator(sample_rate, (counter))
    sample_count = 0
    with WavReader(wav_filename) as wav:
        print(f"the type of wav is {type(wav)}")
        for sample in wav:
            afsk.process_sample(sample)
            sample_count += 1
    print(f"received packets: {counter.count}")
    print(f"sample count is {sample_count}")

def main():
    test_processing_waveform()
    