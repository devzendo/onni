#!/bin/bash
export PICO_SDK_PATH=/opt/pico-sdk
export PICO_EXTRAS_PATH=/opt/pico-extras
if [ "$1" = "clean" ]
then
	rm -rf cmake-build-debug
fi

if [ ! -d cmake-build-debug ]
then
	mkdir cmake-build-debug
	(cd cmake-build-debug ; cmake -DCMAKE_BUILD_TYPE:STRING=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE -DCMAKE_C_COMPILER:FILEPATH=/usr/bin/arm-none-eabi-gcc -DCMAKE_CXX_COMPILER:FILEPATH=/usr/bin/arm-none-eabi-g++ --no-warn-unused-cli -G "Unix Makefiles" ..)
fi
(cd cmake-build-debug ; make -j 4)
pwd
ls -l cmake-build-debug/onni.uf2

