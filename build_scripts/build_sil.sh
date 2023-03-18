#!/bin/bash -x

############################################################
# Help                                                     #
############################################################
Help()
{
        echo "Build Ardupilot SIL and prepare resources, must be run from gust environment."
        echo
        echo "Syntax build_sil_manager.sh [-h]"
        echo "-h        Print the help text."
        echo "-d        When building in docker"
        echo

}

usingDocker=false

while getopts ":hd" option; do
        case $option in
                h) # display help
                        Help
                        exit;;
                d) # docker
                        usingDocker=true
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

echo "Building Ardupilot SIL and copying files to resources"

rm -r ./src/main/resources/base/sil_manager
mkdir ./src/main/resources/base/sil_manager

if [ ${usingDocker} == true ]
then
  cp ./repos/ardupilot_jetson/build/sitl/bin/arducopter ./src/main/resources/base/sil_manager
  cp ./repos/ardupilot_jetson/Tools/autotest/default_params/copter.parm ./src/main/resources/base/sil_manager

else
  session=build_sil

  tmux new-session -d -s ${session}
  tmux send-keys -t ${session} 'conda activate gust_dev' C-m
  tmux send-keys -t ${session} 'python /home/lagerprocessor/Projects/ardupilot/Tools/autotest/sim_vehicle.py --no-mavproxy' C-m

  sleep 10

  tmux kill-session -t ${session}
  cp /home/lagerprocessor/Projects/ardupilot/build/sitl/bin/arducopter ./src/main/resources/base/sil_manager
  cp /home/lagerprocessor/Projects/ardupilot/Tools/autotest/default_params/copter.parm ./src/main/resources/base/sil_manager
  rm -rf ./terrain/
  rm -rf ./logs/
fi

