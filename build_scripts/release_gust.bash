#!/bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Create release of GUST and build dependencies automatically."
        echo
	echo "Assumes it is called from the build_scripts directory."
	echo
        echo "Syntax release_gust.sh [-h|-s|-d]"
        echo "-h	Print the help text."
        echo "-s	Skip building the dependencies (e.g. WGSI apps, radio manager etc.)"
        echo "-d	Flag to pass when being run inside a Docker container"
        echo
}


############################################################
# Process the input options. Add options as needed.        #
############################################################
skip=false
useDocker=false
while getopts ":hsd" option; do
	case $option in
		s) # skip dependencies
			skip=true
			;;
		h) # help
			Help
			exit;;
		d) # use docker container version
			useDocker=true
			;;
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
	./build_radio_manager.sh
	./build_cmr_manager.sh
	./build_zed_manager.sh
fi

cd ..
echo "Cleaning..."
fbs clean

echo "Freezing..."
fbs freeze

mkdir ./target/gust/PyQt5/Qt5/plugins/geoservices/
if [ ${useDocker} == true ]
then
  echo "TODO: Need to copy PyQt5/Qt5/plugins/geoservices/libqtgeoservices_osm.so -> ./target/gust/PyQt5/Qt5/plugins/geoservices/"
  echo "TODO: Need to copy PyQt5/Qt5/plugins/geoservices/libqtgeoservices_itemsoverlay.so -> ./target/gust/PyQt5/Qt5/plugins/geoservices/"
else
  #cp ${CONDA_PREFIX}/bin/gunicorn ./target/gust/
  # hardcode these paths to docker path
  cp ${CONDA_PREFIX}/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_osm.so ./target/gust/PyQt5/Qt5/plugins/geoservices/
  cp ${CONDA_PREFIX}/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_itemsoverlay.so ./target/gust/PyQt5/Qt5/plugins/geoservices/
fi

echo "Packaging..."
fbs installer
