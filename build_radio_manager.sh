#!/bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Build Radio Manager, must be run from gust environment."
        echo
        echo "Syntax build_radiomanager.sh [-h]"
        echo "-h        Print the help text."
        echo
}


while getopts ":h" option; do
        case $option in
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


############################################################
# Main program                                             #
############################################################

echo "Building radio manager app ..."

rm -r ./src/main/resources/base/radio_manager
mkdir ./src/main/resources/base/radio_manager

pyinstaller --onefile --noconfirm --noupx --clean \
	-n radio_manager \
	-p ./gust_packages/radio_manager \
	--hidden-import lxml \
	--hidden-import lxml.etree \
	--hidden-import urllib2 \
	--hidden-import urlparse \
	--collect-all pymavlink \
	--collect-all dronekit \
	--distpath ./src/main/resources/base/radio_manager \
	--workpath ./gust_packages/radio_manager/build \
	--specpath ./gust_packages/radio_manager \
	gust_packages/radio_manager/src/radio_manager/cli.py
