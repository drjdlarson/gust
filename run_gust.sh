#!/bin/bash


Help()
{
	echo "Run GUST for debugging and build dependencies automatically."
	echo
	echo "Syntax run_gust.sh [-h|-b]"
	echo "-h	Print the help text."
	echo "-b	Build the helper executables before running."
	echo
}



while getopts ":hb" option; do
	case $option in
		b) # build wsgi
			./build_wsgi.sh
			./build_radiomanager.sh
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
