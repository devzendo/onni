# onni 

## What is this?
A Raspberry Pi Pico experiment. Not much to see here yet!

## Project Status
Started Nov 2024. Feasibility, building prototypes to reduce risk and develop understanding. 

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
The project was set up using the Raspberry Pi Pico plugin.

# Building
Assuming a macOS or Linux host. Not catering for Windows building any time soon.

Install the Pico SDK and toolchain:

    * `apt install gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential`

    * The Pico SDK 2.1.0 should be cloned from https://github.com/raspberrypi/pico-sdk
    Ensure that the 2.1.0 tag is checked out.
    Ensure that the submodules (specifically tinyusb) are of the correct version for this
    version of the SDK, with:
    'git submodule update --init'
    Set the `PICO_SDK_PATH` environment variable to point to this copy of the Pico SDK.
    
    * CMake can be installed from apt, no need for a manual install.

To build:
`./build.sh clean`

Subsequent builds can just do `./build.sh`



# License, Copyright & Contact info
This code is released under the MIT License: https://mit-license.org/.

(C) 2024 Matt J. Gumbley

matt.gumbley@devzendo.org

Mastodon: @M0CUV@mastodon.radio

http://devzendo.github.io/onni

The code started from the `cdc_uac2` example of the TinyUSB project, whose code is
Copyright (c) 2018-2023, Ha Thach (tinyusb.org),
Angel Molina (angelmolinu@gmail.com), Jerzy Kasenberg,
Dhiru Kholia <dhiru.kholia@gmail.com>

The project also uses the Raspberry Pi Pico SDK, which is 
Copyright 2020 (c) 2020 Raspberry Pi (Trading) Ltd.

I gratefully acknowledge the example code by these authors, without whose efforts
this project could not exist.
