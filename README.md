# onni 

## What is this?
A Raspberry Pi Pico experiment. Not much to see here yet!

## Project Status
Started Nov 2025. Feasibility, building prototypes to reduce risk. 

## What is the meaning of the name?
Onni is a Finnish word, meaning happiness.
That feeling when you're in your shack, tinkering with something...

# Building
Assuming a macOS or Linux host. Not catering for Windows any time soon.

Install the Pico SDK and toolchain:

    `apt install gcc-arm-none-eabi libnewlib-arm-none-eabi build-essential`
    The Pico SDK should be cloned from https://github.com/raspberrypi/pico-sdk
    Set the `PICO_SDK_PATH` environment variable to point to this copy of the Pico SDK.
    The Pico Extras should be cloned into the directory alongside the SDK from https://github.com/raspberrypi/pico-extras
    Set the `PICO_EXTRAS_PATH` environment variable to point to this copy of the Pico Extras.
    i.e. the pico-sdk and pico-extras clones are siblings.
    CMake can be installed from apt, no need for a manual install.


To build: initialise the copy of the tinyusb repo in your pico SDK directory with
'git submodule update --init'.

./build.sh clean

Subsequent builds can just do ./build.sh



# License, Copyright & Contact info
This code is released under the Apache 2.0 License: http://www.apache.org/licenses/LICENSE-2.0.html.

(C) 2024 Matt J. Gumbley and hopefully others!

matt.gumbley@devzendo.org

Mastodon: @M0CUV@mastodon.radio

http://devzendo.github.io/parachute


