#!/bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Build WSGI apps, must be run from gust environment."
        echo
        echo "Syntax build_wsgi.sh [-h]"
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
echo "Building WSGI apps..."

rm -r ./src/main/resources/base/wsgi_apps
mkdir ./src/main/resources/base/wsgi_apps

pyinstaller --onefile --noconfirm --noupx --clean \
	-n wsgi_apps \
	-p ./gust_packages/wsgi_apps \
	--hidden-import gunicorn.glogging \
	--hidden-import gunicorn.workers.sync \
	--distpath ./src/main/resources/base/wsgi_apps \
	--workpath ./gust_packages/wsgi_apps/build \
	--specpath ./gust_packages/wsgi_apps \
	gust_packages/wsgi_apps/src/wsgi_apps/cli.py
