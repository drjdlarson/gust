#!/bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Build Zed Manager, must be run from gust environment."
        echo
        echo "Syntax build_zed_manager.sh [-h]"
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

echo "Building zed manager app ..."

rm -r ../src/main/resources/base/zed_manager
mkdir ../src/main/resources/base/zed_manager

pyinstaller --onefile --noconfirm --noupx --clean \
	-n zed_manager \
	-p ../gust_packages/zed_manager \
	--distpath ../src/main/resources/base/zed_manager \
	--workpath ../gust_packages/zed_manager/build \
	--specpath ../gust_packages/zed_manager \
	../gust_packages/zed_manager/src/zed_manager/cli.py
