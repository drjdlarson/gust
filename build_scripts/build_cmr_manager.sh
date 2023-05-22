#!/bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Build CMR Manager, must be run from gust environment."
        echo
        echo "Syntax build_cmr_manager.sh [-h]"
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

echo "Building CMR manager app ..."

rm -r ./src/main/resources/base/cmr_manager
mkdir ./src/main/resources/base/cmr_manager

pyinstaller --onefile --noconfirm --noupx --clean \
	-n cmr_manager \
	-p ./gust_packages/cmr_manager \
	--hidden-import lxml \
	--hidden-import lxml.etree \
	--hidden-import urllib2 \
	--hidden-import urlparse \
	--collect-all pymavlink \
	--collect-all dronekit \
	--distpath ./src/main/resources/base/cmr_manager \
	--workpath ./gust_packages/cmr_manager/build \
	--specpath ./gust_packages/cmr_manager \
	gust_packages/cmr_manager/src/cmr_manager/cli.py
