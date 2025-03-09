#!/bin/bash
# Doesn't use this when the VSCode-downloaded SDK is available in my home dir's ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake
export PICO_SDK_PATH=/opt/pico-sdk
BUILDFOLDER=build
if [ "$1" = "clean" ]
then
	rm -rf ${BUILDFOLDER}
fi

if [ ! -d ${BUILDFOLDER} ]
then
	mkdir ${BUILDFOLDER}
	cmake -DPICO_TINYUSB_PATH=./libs/tinyusb -DCMAKE_BUILD_TYPE:STRING=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE -DCMAKE_C_COMPILER:FILEPATH=/usr/bin/arm-none-eabi-gcc -DCMAKE_CXX_COMPILER:FILEPATH=/usr/bin/arm-none-eabi-g++ --no-warn-unused-cli -G "Unix Makefiles" -S. -B./${BUILDFOLDER}
fi
(cd ${BUILDFOLDER} ; make -j 4)
pwd
ls -l ${BUILDFOLDER}/onni.uf2

