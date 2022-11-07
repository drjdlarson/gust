#!/bin/bash
echo "Cleaning..."
fbs clean

echo "Freezing..."
fbs freeze

mkdir ./target/gust/PyQt5/Qt5/plugins/geoservices/
cp ${CONDA_PREFIX}/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_osm.so ./target/gust/PyQt5/Qt5/plugins/geoservices/
cp ${CONDA_PREFIX}/lib/python3.7/site-packages/PyQt5/Qt5/plugins/geoservices/libqtgeoservices_itemsoverlay.so ./target/gust/PyQt5/Qt5/plugins/geoservices/

echo "Packaging..."
fbs installer
