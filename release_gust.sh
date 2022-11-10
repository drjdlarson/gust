#!/bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Create release of GUST and build dependencies automatically."
        echo
        echo "Syntax release_gust.sh [-h|-s]"
        echo "-h	Print the help text."
	echo "-s	Skip building the dependencies (e.g. WGSI apps, etc.)"
        echo
}


############################################################
# Process the input options. Add options as needed.        #
############################################################
skip=false
while getopts ":hs" option; do
	case $option in
		s) # skip dependencies
			skip=true
			;;
		h) # help
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
if [ "$skip" = false ] ; then
	./build_wsgi.sh
fi


echo "Cleaning..."
fbs clean

echo "Freezing..."
fbs freeze

mkdir ./target/gust/PyQt5/Qt5/plugins/geoservices/
#cp ${CONDA_PREFIX}/bin/gunicorn ./target/gust/
cp ${CONDA_PREFIX}/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_osm.so ./target/gust/PyQt5/Qt5/plugins/geoservices/
cp ${CONDA_PREFIX}/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_itemsoverlay.so ./target/gust/PyQt5/Qt5/plugins/geoservices/

echo "Packaging..."
fbs installer
