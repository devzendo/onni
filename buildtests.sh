#!/bin/bash
BUILDFOLDER=build
if [ "$1" = "clean" ]
then
	rm -rf ${BUILDFOLDER}
fi

if [ ! -d ${BUILDFOLDER} ]
then
	mkdir ${BUILDFOLDER}
	cmake -DPICO_TINYUSB_PATH=./libs/tinyusb -DCMAKE_BUILD_TYPE:STRING=Debug -DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=TRUE --no-warn-unused-cli -G "Unix Makefiles" -S. -B./${BUILDFOLDER} -DBUILD_TARGET=2
fi
(cd ${BUILDFOLDER} ; make -j 4)


