# Notes on the AFSK modem in tnc1
Input from the radio - ADC.

ADC set to provide 9600 conversions/sec.

Is the ISR turned on/off around half duplex receive phases? 

ADC interrupt:
  Sets an overflow flag if the RX FIFO is full.
  Else subtracts 512 from the sample to put it in the range [-512..+511]
  Attenuates it by shifting it right by the current input gain setting
  Then clamps this at [-128..+127]
  Pushes it into the (not full) RX FIFO.

AFSK Read is asynchronous, and given a buffer / size, will block until
the buffer is full of data pulled from the RX FIFO. While polling the
FIFO for data, if it is empty, the bottom half is called. This waits
for data to be added to the FIFO by the ISR, and processes it into the
AFSK modem object.

The processing of each byte of data read from the FIFO into the AFSK
modem object comprises:
  Taking the min, avg and max of the DC filter buffer array (32 bytes).
  The input volume is set to the difference between max and min.
  The DC filter's current sample is then filtered:
    If there's no carrier present (see below) the RX FIFO is emptied and
    the HDLC layer reset (set to waiting for data).

    The low pass IIR filter is then shuffled x[0] = x[1], and x[1] is set:
    The AFSK's delay FIFO's value is multiplied by the current DC filter
    sample, this is then halved and set in LP IIR x[1].
    LP IIR y[0] = y[1], and:
    y[1] = x[0] + x[1] + (y[0] >> 1)
    (This is an optimised Chebyshev filter - need to study this.)

    The output of this y[1] is shifted left into the AFSK's sampled_bits
    delay line:
    if y[1] is positive, 1 is shifted, if zero, 0 is shifted.

    The DC filter's current sample is pushed into the AFSK's delay FIFO.

    The phase is then adjusted if the sampled_bits delay line has an
    edge (bits ^ (bits >> 1) & 0x01) == 0x01 :
      if the phase is less than the threshold
        add the phase increment
      else
        subtract the phase increment
    The phase is then incremented by the bits-per-sample value (8)
    If the phase is greater than its maximum,
      It is then clipped to be within the max phase
      The bit value is taken from the last three bits of sampled_bits,
      if there two are more bits set in those three, the bit value is 1
      else 0.
      The bit value is passed onto the HDLC decoder.

  The byte read from the ADC is then used to adjust the carrier detection
  data:


  TBC

  The DC filter is then updated with the sample - avg volume, and the
  index into the DC filter is wrapped around the length of the DC filter.
   
