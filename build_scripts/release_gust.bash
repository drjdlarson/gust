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
        echo "-l	Flag to pass when being run locally. Edit the CONDA_PREFIX variable for this case"
        echo
}


############################################################
# Process the input options. Add options as needed.        #
############################################################
skip=false
useDocker=true
while getopts ":hsd" option; do
	case $option in
		s) # skip dependencies
			skip=true
			;;
		h) # help
			Help
			exit;;
		l) # copy the geoservices files using local paths
			useDocker=false
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
	echo "Copying the geoservices files inside docker container"
	# hardcoded the paths to work while running this script inside docker container
	cp /usr/local/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_osm.so /workspaces/gust/target/gust/PyQt5/Qt5/plugins/geoservices/
	cp /usr/local/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_itemsoverlay.so /workspaces/gust/target/gust/PyQt5/Qt5/plugins/geoservices/	
else
  #cp ${CONDA_PREFIX}/bin/gunicorn ./target/gust/
  # hardcode these paths to docker path
  cp ${CONDA_PREFIX}/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_osm.so ./target/gust/PyQt5/Qt5/plugins/geoservices/
  cp ${CONDA_PREFIX}/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_itemsoverlay.so ./target/gust/PyQt5/Qt5/plugins/geoservices/
fi

echo "Packaging..."
fbs installer
