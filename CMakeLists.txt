# Generated Cmake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location
# (note this can come from environment, CMake cache etc)

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.1.0)
set(toolchainVersion 13_3_Rel1)
set(picotoolVersion 2.1.0)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================

# Haven't managed to get this bit working - if you don't have the VSCode Pi Pico extension
# but have the toolchain separately downloaded, and the SDK at a location with the right
# environment variable PICO_SDK set. Picotool just doesn't build correctly - seems to be
# a recent change in the SDK that's broken this, bsp/board_api.h is missing?
if (NOT EXISTS ${picoVscode})
    set(CMAKE_C_COMPILER /usr/bin/arm-none-eabi-gcc)
    set(CMAKE_CXX_COMPILER /usr/bin/arm-none-eabi-g++)
    set(PICOTOOL_FORCE_FETCH_FROM_GIT 1)
endif()

set(PICO_BOARD pico CACHE STRING "Board type")

# Use the submodule of tinyusb in preference to that in the Raspberry Pi Pico SDK
set(PICO_TINYUSB_PATH ${CMAKE_CURRENT_LIST_DIR}/libs/tinyusb)

# Pull in Raspberry Pi Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(onni C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Add executable. Default name is the project name, version 0.1

cmake_minimum_required(VERSION 3.13)

add_executable(onni)

target_sources(onni PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/src/main.c
        ${CMAKE_CURRENT_LIST_DIR}/src/cdc_app.c
        ${CMAKE_CURRENT_LIST_DIR}/src/uac2_app.c
        ${CMAKE_CURRENT_LIST_DIR}/src/usb_descriptors.c
        )

# Make sure TinyUSB can find tusb_config.h
target_include_directories(onni PUBLIC
        ${CMAKE_CURRENT_LIST_DIR}/src)

# In addition to pico_stdlib required for common PicoSDK functionality, add dependency on tinyusb_device
# for TinyUSB device support and tinyusb_board for the additional board support library used by the example
target_link_libraries(onni PUBLIC pico_stdlib pico_unique_id tinyusb_device tinyusb_board)

# Uncomment this line to enable fix for Errata RP2040-E5 (the fix requires use of GPIO 15)
#target_compile_definitions(onni PUBLIC PICO_RP2040_USB_DEVICE_ENUMERATION_FIX=1)

pico_add_extra_outputs(onni)

pico_enable_stdio_usb(onni 1)
pico_enable_stdio_uart(onni 0)

# add url via pico_set_program_url
