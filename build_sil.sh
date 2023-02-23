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

echo "Building Ardupilot SIL and copying files to resources"

rm -r ./src/main/resources/base/sil_manager
mkdir ./src/main/resources/base/sil_manager

session=build_sil

tmux new-session -d -s ${session}
tmux send-keys -t ${session} 'conda activate gust_dev' C-m
tmux send-keys -t ${session} 'python /home/lagerprocessor/Projects/ardupilot/Tools/autotest/sim_vehicle.py --no-mavproxy --vehicle=ArduCopter --location=SHELBY' C-m

sleep 10

tmux kill-session -t ${session}


#python /home/lagerprocessor/Projects/ardupilot/Tools/autotest/sim_vehicle.py --no-mavproxy --vehicle=ArduCopter --location=SHELBY &
#sleep 10

# kill -SIGINT $!
#kill -SIGINT $(ps -o pid= --ppid $$) 

cp /home/lagerprocessor/Projects/ardupilot/build/sitl/bin/arducopter ./src/main/resources/base/sil_manager 
cp /home/lagerprocessor/Projects/ardupilot/Tools/autotest/default_params/copter.parm ./src/main/resources/base/sil_manager 



