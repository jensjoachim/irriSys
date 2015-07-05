#!/bin/bash
BUILD="FALSE"
UPLOAD="FALSE"
BOARD="FALSE"
SERIAL="FALSE"

while [[ $# > 0 ]]
do
key="$1"

case $key in
	-b|--build)
	BUILD="TRUE"
	;;
	-u|--upload)
	UPLOAD="TRUE"
	;;
	-m|--board)
	BOARD="$2"
	shift
	;;
	-p|--serial)
	SERIAL="$2"
	shift
	;;
	*)

	;;
esac
shift
done
#echo BUILD = "${BUILD}"
#echo UPLOAD = "${UPLOAD}"
#echo BOARD = "${BOARD}"
#echo SERIAL = "${SERIAL}"
#echo PWD = "${PWD}"

if [ ${BUILD} == "TRUE" ]
then
	build_s="ino build"
	if [ ${BOARD} != "FALSE" ]
	then
		build_s=$build_s" -m "$BOARD
	fi
	echo $build_s
	# Maybe also remove the directory
	cp -r ../arduino_code/* ../../ino/workspace/
	cd ../../ino/workspace
	$build_s
	cd ../../irriSys/raspi_code
fi

if [ ${UPLOAD} == "TRUE" ]
then
	upload_s="ino upload"
	if [ ${BOARD} != "FALSE" ]
	then
		upload_s=$upload_s" -m "$BOARD
	fi
	if [ ${SERIAL} != "FALSE" ]
	then
		upload_s=$upload_s" -p "$SERIAL
	fi
	echo $upload_s
	cd ../../ino/workspace
	$upload_s
	cd ../../irriSys/raspi_code
fi
