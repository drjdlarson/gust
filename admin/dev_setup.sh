# !bin/bash

echo ""
echo "Making Link for designer"
ln -sf /usr/local/lib/python3.7/site-packages/qt5_applications/Qt/bin/designer /usr/bin/designer

echo ""
echo "Getting binary package for ardupilot"

echo ""
echo "Generating documentation and opening documentation API"
cd build_scripts 
./build_documentation.sh -o