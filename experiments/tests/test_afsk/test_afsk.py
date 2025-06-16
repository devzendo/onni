# tests/test_core.py
import pytest
from experiments.afsk import AfskCorrelator

def test_dummy():
    afsk = AfskCorrelator()
    assert afsk.dummy() == 1
    
    