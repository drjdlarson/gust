#!/bin/bash


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

	echo
}



while getopts ":hawrcz" option; do
	case $option in
		a) # build all helping executables
			./build_wsgi.sh
			./build_radio_manager.sh
			./build_cmr_manager.sh
			./build_zed_manager.sh
			;;
		w) # build wsgi app
			./build_wsgi.sh
			;;
		r) # build radio manager
			./build_radio_manager.sh
			;;
		c) # build cmr manager
			./build_cmr_manager.sh
			;;
		z) # build zed manager
			./build_zed_manager.sh
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
