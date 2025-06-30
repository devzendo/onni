from abc import ABC, abstractmethod
from typing import List

class PacketObserver(ABC):
    @abstractmethod
    def notify(self, packet):
        pass

class AfskCorrelator:
    def __init__(self, *observers: List[PacketObserver]):
        self.observers = observers
        print(f"observers are {self.observers}")

    def notify_packet(self, packet):
        for obs in self.observers:
            obs.notify(packet)

    def process_sample(self, sample):
        print("sample: %s" % (hex(sample[0])))
        pass