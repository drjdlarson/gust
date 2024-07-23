#!/bin/bash


# TODO: Get this working in a more simple way see if the binary package can be put in the container, and in a standardized location
    # also figure out what that would mean for everything using ardupilot

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Build Ardupilot SIL and prepare resources."
        echo "Copies the Ardupilot vehicle executables to GUST resources."
        echo
        echo "Before running this script, a binary executable of Ardupilot SITL must be present in ardupilot/build/sitl/bin/"
        echo 
        echo "Follow the instructions from https://ardupilot.org/dev/docs/SITL-setup-landingpage.html to setup SITL and get a binary executable."        
        echo "This needs to run outside the docker container. You will pass the absolute file path of ardupilot directory as argument to this script."
        echo "Syntax build_sil_manager.sh /path/to/ardupilot"
        echo 
        echo "Example path: /home/lagerprocessor/Projects/ardupilot"
        echo 
        echo "-h        Print the help text."
        echo

}

while getopts "p:h:" option; do
    case $option in  
        p) # store file path in path variable
            path=${OPTARG}
            ;;
        h) # display help
            Help
            exit;;
        \?) # invalid argument
            echo "Invalid argument"
            echo
            Help
            exit;;
    esac
done

############################################################
# Main program                                             #
############################################################

echo "Building Ardupilot SIL and copying files to resources"

echo
echo "The absolute path of ardupilot dir is "
echo $path

rm -rf ../../src/main/resources/base/sil_manager
mkdir ../../src/main/resources/base/sil_manager

echo "Copying ArduCopter Stuff"
cp $path/build/sitl/bin/arducopter ./src/main/resources/base/sil_manager
cp $path/Tools/autotest/default_params/copter.parm ./src/main/resources/base/sil_manager

# echo "Copying ArduPlane Stuff"
# cp $path/build/sitl/bin/arduplane ../src/main/resources/base/sil_manager
# cp $path/Tools/autotest/default_params/plane-jet.parm ../src/main/resources/base/sil_manager

rm -rf ../terrain/
rm -rf ../logs/


