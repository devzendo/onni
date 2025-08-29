# onni 

## What is this?
A Raspberry Pi Pico experiment. Not much to see here yet!

The intention is to build a triple-mode interface between a computer and an amateur radio
transceiver. The three possible modes are (intended to be):
1. A sound card. Audio from the computer causes the transceiver's PTT (Push To Talk button)
   to be activated, and the audio transmitted on the current frequency. When the audio from
   the computer stops, the received audio from the transceiver is sent to the computer. This
   allows the use of software such as WSJT-X, Direwolf, etc. This is similar to the Digirig
   or Tigertronics Signalink interface.
2. A KISS modem. Packet software running on the computer uses the board to send/receive
   packets encapsulated in the KISS protocol. The board activates PTT and modulates the
   data in the appropriate form. Packets received and demodulated are sent to the computer
   in KISS frames. This is similar to the Mobilinkd TNC interface, and can be used with
   Direwolf and APRS software.
3. A standalone TNC (Terminal Node Controller). The user interface is used to issue connections
   to remote AX25 nodes, send beacons, digipeat, and access the mailbox. Like the TNCs of the
   80's. The board handles PTT and modulation as in mode 2, but has a complete AX25 stack and
   applications embedded.

It presents an audio (mic, stereo speakers) interface and two CDC 'serial' ports.
The audio interface acts as a sound card; the two serial ports are for:

* The text-based user interface. Connect to it with a decent VT100 terminal emulator such as
  minicom or PuTTy.
* A KISS (Keep It Simple, Stupid) interface.

## Project Status
Started Nov 2024. Feasibility, building prototypes to reduce risk and develop understanding. 
Experimenting with AX25 packet demodulation.
Last updates in Aug 2025.

## What is the meaning of the name?
Onni is a Finnish word, meaning happiness.
That feeling when you're in your shack, tinkering with something...

# Releases
Binary releases (.UF2 files) will be made available from the project's github page. 
Drag and drop them onto a fresh Raspberry Pi Pico to flash them onto the device.

# Hardware requirements
A breadboard build of onni will be documented. For now, just a Pi Pico 1 is needed.
Eventually you'll need a handful of discrete components in addition to this.... more on this later.

# Development
I use Visual Studio Code (on macOS) connected remotely to a Linux Mint 21.3 (Ubuntu 22.04) PC.
Or use Visual Studio Code directly on that PC.
The project was set up using the Raspberry Pi Pico plugin.

# Development Setup
Assuming a Linux host. Not catering for Windows building any time soon.

Install the Pico SDK and toolchain:

    * `apt install gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential`

    * The Pico SDK 2.1.0 should be cloned from https://github.com/raspberrypi/pico-sdk
    Ensure that the 2.1.0 tag is checked out.
    Ensure that the submodules (specifically tinyusb) are of the correct version for this
    version of the SDK, with:
    'git submodule update --init'
    Set the `PICO_SDK_PATH` environment variable to point to this copy of the Pico SDK.
    
    * CMake can be installed from apt, no need for a manual install.

    * TinyUSB is used as a git submodule in `libs/tinyusb`, rather than the version
      shipped with the Pico SDK - to fix various audio problems:
      https://github.com/hathach/tinyusb/issues/628
      https://github.com/hathach/tinyusb/pull/1802
      https://github.com/hathach/tinyusb/issues/1911
      I'm currently using commit 29ffd57237554b1f2339af543e3789ae04d3b29b (8 Mar 2025).

# Building
This project is developed with Test-Driven Development, to the maximum extent possible,
whilst being pragmatic. There are several parts that are tested manually - USB interaction
mostly - with the aim that the rest of the system is tested. The goal is that if the tests
pass, the product can be shipped.

The tests are built and run on the host computer, so, using the desktop Linux C++ compiler,
GoogleTest, and C++ standard library.

The firmware builds using the ARM GCC compiler and Pico SDK; it gets deployed to a Pico.

You can build either - but not both - at the same time. You'll need to clean out/rebuild
the CMake build tree when switching. 

## Building the firmware
To build:
`./build.sh clean`

Subsequent builds can just do `./build.sh` or (cd build && make)

## Building unit tests
`./buildtests.sh clean`

To run the tests:
`./runtests.sh` or (cd build && make && make test)

# Deployment
Usual Pi Pico steps, hold down BOOTSEL button, connect. File browser appears. Drag `build/onni.uf2`
to the 'RPI-RP2' drive. The Pico will then reboot into the onni firmware.

Looking in `/var/log/kern.log` will show a USB audio and CDC (serial) device(s).

You will need to add your user to the `dialout` group in order to connect to the serial device(s):
`sudo adduser matt dialout` then log out/in.

Install `minicom`, and connect to onni's diagnostic output serial port with:
`minicom -b 115200 -o -D /dev/ttyACM0`


# License, Copyright & Contact info
This code is released under the MIT License: https://mit-license.org/.

(C) 2024-2025 Matt J. Gumbley

matt.gumbley@devzendo.org

Mastodon: @M0CUV@mastodon.radio

http://devzendo.github.io/onni

# AI Declaration
Some of the code in the 'experiments' folder (hexdump.py) was generated by Claude
from C++ in the 'src' folder, and reviewed by me.
I use Claude.ai occasionally for assistance; all its output is vetted thoroughly
by me. I also use the Mistral LLM locally hosted.

I gratefully acknowledge the work of others that was stolen without consent in the
creation of Large Language Models. I understand the environmental impact of this
technology.

# Acknowledgements and works used as sources/inspiration
The code started from the `cdc_uac2` example of the TinyUSB project, whose code is
Copyright (c) 2018-2023, Ha Thach (tinyusb.org),
Angel Molina (angelmolinu@gmail.com), Jerzy Kasenberg,
Dhiru Kholia <dhiru.kholia@gmail.com>

The project also uses the Raspberry Pi Pico SDK, which is 
Copyright 2020 (c) 2020 Raspberry Pi (Trading) Ltd.

Setup of googletest was greatly aided by at article at 
https://lochnerweb.de/index.php/pico_unit_testing

Recordings of packet audio in the `samples` directory from the WA8LMF TNCTest CD
and Sivan Toledo's javAX25 project.

The demodulator is based on Sivan Toledo's javAX25 demodulator. I've ported this
to Python 3 in the experiments folder, to aid my understanding and experiment with
it. If successful, I'll port it again to C++ for the embedded version.

Sivan's article in QEX 'A High-Performance Sound Card AX.24 Modem', available at
https://www.tau.ac.il/~stoledo/Bib/Pubs/QEX-JulAug-2012.pdf led me to his project
at https://github.com/sivantoledo/javAX25 that I use (in ported form) here. 

The book 'Digital Signal Processing: A practical guide for engineers and scientists'
by Steven W. Smith (ISBN 0-7506-7444-X) has been invaluable in helping me understand
these concepts. Highly recommended as an introduction to DSP. It is also available
freely online at https://dspguide.com

I gratefully acknowledge the example code by these authors, without whose efforts
this project could not exist.
