#!/bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Build SIL Manager, must be run from gust environment."
        echo
        echo "Syntax build_sil_manager.sh [-h]"
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

echo "Building SIL manager app ..."

rm -r ./src/main/resources/base/sil_manager
mkdir ./src/main/resources/base/sil_manager

pyinstaller --onefile --noconfirm --noupx --clean \
	-n sil_manager \
	--hidden-import lxml \
	--hidden-import lxml.etree \
	--hidden-import urllib2 \
	--hidden-import urlparse \
	--collect-all pymavlink \
	--collect-all dronekit \
	--distpath ./src/main/resources/base/sil_manager \
	--workpath ./gust_packages/sil_manager/build \
	--specpath ./gust_packages/sil_manager \
	dronekit-sitl
