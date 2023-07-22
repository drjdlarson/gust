#!/bin/bash

Help()
{
	echo "Run GUST for debugging and build dependencies automatically."
	echo
	echo "Syntax run_gust.sh [-h|-b]"
	echo "-h	Print the help text."
	echo "-a	Build all the helper executables before running (except SIL)."
	echo "-w	Build the wsgi app helper executable before running."
	echo "-r	Build the radio_manager helper executable before running."
	echo "-c	Build the cmr manager helper executable before running."
	echo "-z	Build the zed manager helper executable before running."
	echo "-s	Build the Ardupilot sil helper executable before running."
	echo "-s	Build the documentation before running."

	echo
}



while getopts ":hawrczs" option; do
	case $option in
		a) # build all helping executables
			cd ./build_scripts
			./build_wsgi.sh
			./build_radio_manager.sh
			./build_cmr_manager.sh
			./build_zed_manager.sh
			./build_documentation.sh
			cd ..
			;;
		w) # build wsgi app
		  cd ./build_scripts
			./build_wsgi.sh
			cd ..
			;;
		r) # build radio manager
			cd ./build_scripts
			./build_radio_manager.sh
			cd ..
			;;
		c) # build cmr manager
		  cd ./build_scripts
			./build_cmr_manager.sh
			cd ..
			;;
		z) # build zed manager
			cd ./build_scripts
			./build_zed_manager.sh
			cd ..
			;;
	  s) # build zed manager
			cd ./build_scripts
			./build_sil.sh
			cd ..
			;;
	  d) # build documentation
	    cd ./build_scripts
	    ./build_documentation.sh
			cd ..
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