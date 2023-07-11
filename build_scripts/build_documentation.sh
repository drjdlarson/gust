#!/bin/bash

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Create documentation of gust using sphinx and generate html."
        echo
	echo "Assumes it is called from the build_scripts directory."
	echo
        echo "Syntax release_gust.sh [-h|-o]"
        echo "-h	Print the help text."
        echo "-o	Open the final documentation (index.html) in Chrome browser"
        echo
}


############################################################
# Process the input options. Add options as needed.        #
############################################################
display_in_browser=false
while getopts ":ho" option; do
	case $option in
		o) # skip dependencies
			display_in_browser=true
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
echo "Building documentation ..."

echo "Clearing previous documentation files"
rm -rf ./docs/build/
rm -rf ./docs/source/packages_api/
rm -rf ./docs/source/_static/
rm -rf ./docs/source/_templates/
rm -rf ./docs/source/_autosummary/

mkdir ./docs/source/packages_api

echo "Generating source for GUST"
sphinx-apidoc --force --tocfile gust_module --no-headings --module-first -o ./docs/source/packages_api ./src/main/python/gust/

echo "Generating source for RadioManager"
sphinx-apidoc --force --tocfile radio_manager_module --no-headings --module-first -o ./docs/source/packages_api ./gust_packages/radio_manager/src/radio_manager/

echo "Generating source for WSGI App"
sphinx-apidoc --force --tocfile wsgi_apps_module --no-headings --module-first -o ./docs/source/packages_api ./gust_packages/wsgi_apps/src/wsgi_apps/

echo "Generating source for Utilities"
sphinx-apidoc --force --tocfile utilities_module --no-headings --module-first -o ./docs/source/packages_api ./utilities/src/utilities/

echo "Generating source for Utilities"
sphinx-apidoc --force --tocfile zed_manager_module --no-headings --module-first -o ./docs/source/packages_api ./gust_packages/zed_manager/src/zed_manager/


cd ./docs
make clean
make html

if [ "$display_in_browser" = true ] ; then
  google-chrome file:///workspaces/gust/docs/build/html/index.html --no-sandbox
fi