#!/bin/bash

scriptDir=./build_scripts

Help()
{
	echo "Run GUST for debugging and build dependencies automatically."
	echo
	echo "Syntax run_gust.sh [-h|-b]"
	echo "-h	Print the help text."
	echo "-a	Build all the helper executables before running."
	echo "-w	Build the wsgi app helper executable before running."
	echo "-r	Build the radio_manager helper executable before running."
	echo "-c	Build the cmr manager helper executable before running."
	echo "-z	Build the zed manager helper executable before running."
	echo "-s	Build the Ardupilot sil helper executable before running."

	echo
}



while getopts ":hawrczs" option; do
	case $option in
		a) # build all helping executables
			${scriptDir}/build_wsgi.sh
			${scriptDir}/build_radio_manager.sh
			${scriptDir}/build_cmr_manager.sh
			${scriptDir}/build_zed_manager.sh
			${scriptDir}/build_sil.sh
			;;
		w) # build wsgi app
			${scriptDir}/build_wsgi.sh
			;;
		r) # build radio manager
			${scriptDir}/build_radio_manager.sh
			;;
		c) # build cmr manager
			${scriptDir}/build_cmr_manager.sh
			;;
		z) # build zed manager
			${scriptDir}/build_zed_manager.sh
			;;
	  s) # build zed manager
			${scriptDir}/build_sil.sh
			;;
		h) # display help
			Help
			exit;;
		\?) # invalid
			echo "Error: Invalid option"
			echo
			Help
			exit;;
	esac
done


fbs run
