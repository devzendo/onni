
import array
import wave

from experiments.afsk import AfskCorrelator, PacketObserver
from experiments.hexdump import hexdump

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


wav_filename = "../samples/01_40-Mins-Traffic-on-144.39.wav"
class Counter(PacketObserver):
    def __init__(self):
        self.count = 0
        
    def notify(self, packet):
        print(f"got a packet {packet}")
        hexdump(packet, len(packet))
        self.count+=1

def main():
    print("This is the main demodulator harness")
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

if __name__ == "__main__":
    main()
