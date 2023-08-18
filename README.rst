GUST
====


.. image:: docs/source/images/gust_logo.png
    :width: 360

..
    BEGIN INTRO INCLUDE

The Ground Control Station (GCS) for Uncrewed Swarms and Teams (GUST) is an application developed by the `Laboratory for Autonomy, GNC, and Estimation Research (LAGER) <http://lager.ua.edu/>`_ at The University of Alabama. GUST offers comprehensive planning, tracking, command, and control capabilities of an uncrewed swarm for teaming operations. It utilizes the standard MAVLink protocol to communicate with the swarm agents, enabling compatibility with various uncrewed autonomous systems such as Ardupilot based flight computers and Bolder Flight Systems. Full-stack development of GUST was done primarily based on PyQt5 framework. Its software architecture is designed to be modular for easy integration of external plugins and software packages. The GUST application runs inside a docker container making it compatible with any operating system with docker. It is also deployed on a ruggedized ground station box for LAGER’s outdoor survey and remote sensing operations with Uncrewed Aircraft Systems (UAS).

Major Features:

* Capable of relaying real-time telemetry from all connected vehicles to a single Graphical User Interface (GUI) for convenient monitoring.
* Easy integration of external plugins and tools.
* Includes a Target tracking module with a GUI to configure and display real time tracking information from different sensors (example: ZED).
* Includes a Planning module to design flight paths for individual vehicles or cooperative maneuvers for a swarm.
* Provides ability for the ground station operator to command and control each vehicle for some specific tasks or during emergencies.
* Storage of flight data from all vehicles for future analysis.

..
    END INTRO INCLUDE


Overview
========

.. image:: docs/source/images/gust_schematic.png

..
    BEGIN OVERVIEW INCLUDE

* Frontend includes all the UI design from QtDesigner and logic for all UI windows. To interact with the backend / database, it sends HTTP requests to WSGI App. These requests are sent as URLs formatted with requested information / commands. The HTTP requests typically return a dict to the Frontend that can be displayed in the UI with appropriate formatting.
* WSGI App routes the HTTP requests to specific classes (in wsgi_apps/api/resources/) to perform certain tasks based on the requests' URL.
* Dashed ellipses in above diagram represent components that spawn separate sub-processes. Start / end of these subprocesses are handled by the backend. All these processes have access to the common database.
* radio_manager package handles all communication with the vehicle radios. It includes methods to connect, send, and receive MAVLink messages from the vehicle using dronekit's API.

    * Note : Each radio_manager process is linked to a unique vehicle and is only responsible for communicating with that vehicle. These radio_manager processes run independently enabling multiple vehicle connection.

* All processes are capable of sending messages to the backend via UDP sockets (handled by gust/conn_manager).
* sqlite is used for database. All processes write information to the database, and WSGI app extracts it from the database for frontend display.

..
    END OVERVIEW INCLUDE



DEV Setup
=========
..
    BEGIN DEV SETUP INCLUDE

Prerequisites
#############

It is recommended to use Visual Studio Code with Docker Dev Container extension for development of GUST. Development containers allow the full toolchain to be automatically setup on most any machine capable of running Docker. 

* Docker and VS Code: For information and instructions on setting up dev-container, see `here <https://code.visualstudio.com/docs/devcontainers/containers>`__ for an overview, `here <https://stackoverflow.com/questions/71402603/vs-code-in-docker-container-is-there-a-way-to-automatically-install-extensions>`__ for auto installing extensions in the container and `here <https://pspdfkit.com/blog/2020/visual-studio-code-cpp-docker/>`__ for an example setup. The provided dev container also has useful extensions installed to ease development.

* Git : For getting started with git, see `here <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`__. If working on Windows, it is recommended to use some emulation tool such as `git Bash <https://www.educative.io/answers/how-to-install-git-bash-in-windows>`__ for using git in command-line interface. Further, it is recommended to add your SSH key to the ssh-agent for authentication. Instructions for checking for existing ssh keys, generating new keys, and adding to github are `here <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent>`__.

* For Windows, run this git command to use Unix style line endings. (Required for the shell scripts. See `here <https://unix.stackexchange.com/a/626437>`__)

    .. code-block:: 

        git config --global core.autocrlf false 




Instructions
############

#. Clone the repo.

    .. code-block:: 

        git clone git@github.com:drjdlarson/gust.git
        cd gust
        git submodule init 
        git submodule update

#. Open VS code and navigate to the cloned directory. At this point, VS code should prompt to 'Reopen in Container', click yes. If the prompt doesn't show up, you can go to the command palette and type "Reopen in Container". Now your terminal within VS Code will be running commands within the container but the files you are editing/creating will be accessible from your local machine's file browser.

    * Note: First setup will take some time to setup. After the container starts running, it runs one script to setup some additional stuff (See Dockerfile and .devcontainer.json). 
    * Note: At this point, your working-directory should be "/workspaces/gust/" in your terminal. 
    * Note: You can still use git commands locally (outside the container).

#. At this point, dev environment should be ready for further work. Run the following command to make sure a window shows up. 

    .. code-block:: 

        ./run_gust.bash


See API reference for overview, software architecture, guide, and documentation of packages before starting development with GUST. 

..
    END DEV SETUP INCLUDE

Install and Usage
=================

..
    BEGIN USAGE INCLUDE

The image with installed GUST package is published in DockerHub under `ualager <https://hub.docker.com/repository/docker/ualager/gust-lager/general>`__. The user can pull the image and open a container using the image. The container should open the software automaticallly and no other steps are necessary.

Prerequisites
#############

* Docker: You must have Docker Daemon running before running the gust-image. You can verify that it is working by running the command :code:`docker run hello-world`. If not, follow the instructions `here <https://docs.docker.com/engine/install/>`__ to install docker engine. 

* Manage host names on the list of machines from which the X server accepts connections. For that, run the following commands, 
    
    .. code-block::

        xhost +local:host
        xhost +local:docker


Installation
############

#. Open terminal and run 

    .. code-block::

        docker run --rm -it --network host --privileged -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev:/dev -v /home/${USER}/Documents:/Documents ualager/gust-lager:v2.0.3
    
* Note: Here we are setting the DISPLAY environment variable and mounting X-server volume in the container to make the display compatible (See `here <https://leimao.github.io/blog/Docker-Container-GUI-Display/>`__). 
* Note: We give the container access to all devices on host and mount the /dev volume for USB ports (used by radio connections).
* Note: We mount the :code:`Documents` directory of the User inside the docker container. So, files used in GUST (exaple: mission files, config files, etc) can be stored in your local /Documents directory and can be accessed inside the containers. 

This should open two GUST windows. First, start the server on one of them. If there are no errors while starting the server, then open Client on the second window. If the server fails to start, try running :code:`./kill_server` in the container terminal. 

Post-Installation
#################

GUST can use offline satellite images for the map. Get the offline map tiles and save them inside :code:`/Documents/gust_resources/offline_folders` before use. If the maps are not saved in the correct location, GUST map widget will display blank. Note that it can also be configured to use other online map plugins such as OSM. Also, see guide for instructions on adding more areas on the map. 
 
 
..
    END USAGE INCLUDE


API Reference
=============

To generate new documentation, run the script. 

    .. code-block:: 

        cd ./build_scripts && ./build_documentation.sh -o

If running inside dev container, this should open the documentation in Google Chrome. 

Cite
====
..
    BEGIN CITE INCLUDE

Please cite the framework as follows

.. code-block:: bibtex

    @Misc{gust,
    author       = {Jordan D. Larson and Aabhash Bhandari and Ryan W. Thomas},
    howpublished = {Web page},
    title        = {{GUST}: A {G}round control station (GCS) for {U}ncrewed {S}warms and {T}eams},
    year         = {2022},
    url          = {https://github.com/drjdlarson/gust},
    }


..
    END CITE INCLUDE
