
Guide
*****

Software Architecture
=====================

.. image:: images/gust_schematic.png

.. include:: ../../README.rst
    :start-after: BEGIN OVERVIEW INCLUDE
    :end-before: END OVERVIEW INCLUDE

Data Flow
=========


Vehicle connection/disconnection
################################

#. When pushbutton_addvehicle is clicked on the main frontend main window, it opens the ConWindow.
#. ConWindow provides several options to the user for vehicle connection. The primary option is the connection type. Based on connection type, other several options are dynamically updated.

    * Radio : MAVLink connection to a radio hardware. User should input vehicle name, select radio port, select baud rate, vehicle color.
    * Ardupilot SIL : MAVLink connection to a SIL on a local TCP port. User should select name and color from dropdowns. Names are populated with the list of SIL names currently running (SIL names are entered when starting a SIL from StartSILWindow). Other options are disabled.
    * Test : Random values imitating MAVLink messages. User should select name and color.

#. Once pushbutton_connect is clicked on ConWindow, it forms an URL including all the selected information for the HTTP Web request.
#. This request is sent to WSGI App which routes the request to ConnInfo class in wsgi_apps/api/resources/drone_namespace
#. ConnInfo class takes all parameters from the received URL and packages into a dictionary. It adds the new connection information in the database and create all necessary tables.
#. Once the vehicle is added to database, it sends the packaged dictionary to ConnServer which is listening to messages on a UDP server socket. To do this, the dictionary is formatted a certain way using utilities.send_info_to_udp_server().
#. When ConnServer receives this message, it spawns a new RadioManager's QProcess for the radio connection. It passes all received information such as name, port, color, baud as arguments to the process. The entrypoint of this new process is radio_manager/cli. Based on received arguments, the radio_manager process starts a dronekit connection with the vehicle. A timeout is also used in the dronekit connection to make sure we wait enough. (Connections with Ardupilot using Dragonlink takes a couple of minutes in some cases.)

    * Note : The dronekit connection string currently used is :code:`radio = dronekit.connect(port, baud=baudrate, timeout=200, heartbeat_timeout=200, wait_ready=True)`

    * Note : ConnServer assigns a unique UDP address to each radio_manager process. When the process is started, it starts a UDP server socket on that address so that each radio_manager can also be a message listener. This allows other UDP clients (typically ConnServer) to send messages to the radio_manager process.

#. Once the process is successfully started, a response message is sent from ConnServer to Frontend via the same route. This response can also include error message if something fails along the way. If everything is successful, the frontend will add the vehicle in the tableWidget and start updating telemetry data.

    * Note : Disconnection also works the same way. Information flows from Frontend -> WSGI apps -> ConnServer and back for response message. For disconnection, only the vehicle name is passed. When ConnServer receives the disconnection message, it kills the radio_manager process associated with the vehicle.


Starting Ardupilot SIL
######################

#. Running an Ardupilot SIL requires a compiled executable on resources/base/sil_manager. (Currently only supporting Arducopter)
#. Once pushbutton_sil is clicked, it opens the StartSILWindow.
#. User can select different options for the SIL. Similar to ConWindow, it creates a URL for HTTP request and sends it to WSGI App.

    * Note : saved locations for spawing the SIL vehicle are in resources/base/locations.txt

#. Data flow is similar to Steps 4-6 from above Vehicle connection/disconnection section
#. When ConnServer receives this message, it spawns a new SIL QProcess. Similar to radio_manager, it assigns a unique TCP port to each SIL process for communication.
#. Once the process is successfully started, user can connect to the SIL by following all the steps in Vehicle connection/disconnection section above

    * Note : Once a radio is disconnected, it kills the SIL process associated with the vehicle along with its radio_manager process.


MAVLink commands from user to vehicle
#####################################

#. MAVLink messages from the vehicle such as vehicle state are constantly pulled by RadioManager. This telemetry data is stored in the common database.
#. FrontendWindow.update_request() method requests the telemetry data from the database in a constant interval using a helper DataManager class.
#. DataManager sends the HTTP requests to the WSGI App. WSGI App includes classes to handle telemetry data requests.
#. These classes include a 'params' attribute which is a list of all the parameters (or vehicle states) that class can request. It pulls the latest value stored for each of the params in the database tables.

    * Note : The strings in the params list are hardcoded in the database side as well. Basically, these params are the headers for the tables in database. So, please do not change these 'params' if you are not sure what you are doing.

#. The return from the database is packaged as a dict including values for all requested parameters for all vehicles.
#. This dict is passed to the frontend window as a return of the HTTP request.
#. Frontend window's DataManager class reorganizes the received dicts into a single dict containing all telemetry data for all vehicles. Once this is done, it emits a signal which is caught by the FrontendWindow.update_frame() method.
#. FrontendWindow.update_frame() updates the UI everytime new data is received from the DataManager.


Backend data handling by ConnServer
###################################

#. At the beginning of the program, the backend starts ConnServer as a thread. ConnServer includes a UDP server socket that constantly listens to messages from other processes.
#. If a message is received from a socket client, it tries to determine the message type.

    * Note : All UDP socket messages used in GUST are always sent with a 'message_type'. Message types are defined in utilities.ConnSettings.

#. Based on the message_type, ConnServer forwards the message to appropriate methods as arguments.
#. It can also send response to the UDP socket clients.

Database Structure
==================

GUST is currently using a sqlite database to store all data. Methods for interacting with the database are included in the Utilities package in :code:`utilities/src/utilities/database.py`. And the sqlite database file is stored in :code:`src/main/resources/base/gust_database.sqlite`. The database can be accessed by all subprocesses.

The database is started when the Server is opened. It contains 4 main tables when it is first started. Check the database.py file to get more details on the specifics of the string. 

#. PluginCollection: This stores information about external plugins with GUST.

#. drone_collection: Stores information for all drones connected to GUST. 

#. locations: Stores information about saved locations. This can be configured in :code:`src/main/resources/base/locations.txt`.

#. zed_collection: Stores information about the connected ZEDs.

Once a new ZED or a vehicle is connected, a new table is created. These new tables store the data coming from the source. 

    * Note: Each Drone connection creates 4 new tables and are named using Enums. These 4 tables store all the telemetry data from the vehicle. DONOT change the strings in the database files if you are unsure, because these strings are called by other packages (wsgi_apps and radio_manager).

    * Note: Each Zed connection creates a table to store all the data being received. 


Instructions
============

Building new UI windows with QtDesigner
#######################################

#. The UI for all windows are designed using QtDesigner. You can use the Designer app inside the docker container. Open Designer app by running

    .. code-block::

        qt5-tools designer

#. Design your UI. Please be consistent with the naming of Qt objects with current style (i.e. include Qt object type in the name).

    * Example : If adding a pushbutton (QPushButton) to open a file, name it ``pushButton_openfile``. If adding a dropdown (QComboBox) to display available colors, name it ``comboBox_colors``.

#. Once you save the file, go to the terminal (inside gust's root directory) and run the python script to convert UI files to python files.

    .. code-block::

        python utilities/src/utilities/convert_ui_files.py

#. The python files with the same name will be saved in gust.gui.ui directory. You should be able to run the converted python file to preview the UI (just like in Designer).

    * Note : Never make any edits to any of the autogenerated python files.

#. To write logic for the new window, create a new python file in gust.gui. Import the autogenerated python file and create a new class for the window inheriting from the UI class in the autogenerated python file. This gives you access to all the UI elements in the new gust.gui file (See examples).

    * Note : This is done to keep the code for window's logic and UI aspects separate. This just makes things cleaner as we have so many windows for gust.


Add more areas in the map
#########################

* Step 1
* Step 2

Adding more Ardupilot SIL models
################################

To run a SITL with GUST, it needs a binary executable from Ardupilot. For that, you need to have Ardupilot SITL setup locally on your device and we can basically copy the executable from your local device to GUST.

You can follow the instructions for setting up Ardupilot SITL `here <https://ardupilot.org/dev/docs/SITL-setup-landingpage.html>`__. Instructions for setting up the build environment on Linux machine is `here <https://ardupilot.org/dev/docs/building-setup-linux.html#building-setup-linux>`__. 

To generate the binary files, you can run 

    .. code-block::

        cd ardupilot/Arducopter
        sim_vehicle.py --no-mavproxy

The binary files will be located in :code:`ardupilot/build/sitl/bin/`.

Once the executable files are created, simply run the script :code:`./build_scripts/build_ardupilot_sil.sh` by passing absolute path of ardupilot's root directory. It basically copies the executables and puts them inside GUST's resources.

For example, on GUST's root directory, run

    .. code-block::

        ./build_scripts/build_ardupilot_sil.sh -p /home/lagerprocessor/Projects/ardupilot

Now, you should be able to run SITL with GUST normally. If you need to add new vehicle type, just run the sim_vehicle.py inside respective directory and it should generate the executable file. You'll also need to modify the build_ardupilot_sil.sh script to copy the new executable.


Code Formatting
###############

Please follow the code style and conventions used in each package. The scripts are formatted using Black and the docstrings should follow NumPy's style. 

After you are done editing, just run Black command at docker's project root (i.e. /workspaces/gust#) for formatting all the source code properly. 

    .. code-block::

        black .
        

Packaging and deploying GUST
############################

GUST is packaged using the fbs tool. fbs is included as a submodule inside the GUST repo. It creates a :code:`*.deb` package for GUST. For compatibility among different host machines, docker is used to deploy the software. A docker image is created that stores the .deb package and installs it. The image can be pulled from DockerHub by any device and can be run. Follow these steps to package and deploy the software. 

#. Once you have added a feature and want to make a release, merge the feature branch to the main branch and push to remote. You will follow the remaining steps while on the main branch.

#. Run the python script :code:`package_gust.py` with appropriate arguments. You should set the version of the new package. Run :code:`python package_gust.py --help` to see the argument options. 

    * Note: This script creates a new version tag for the software (defined in :code:`src/build/settings/base.json`) and runs the :code:`build_scripts/release_gust.bash` script creating a :code:`*.deb` package for GUST. 

    * Note: Check :code:`target/` directory. It should include a :code:`*.deb` file and also an installed gust directory. You should be able to run it with :code:`target/gust/gust` in the terminal. 

#. Run the python script :code:`deploy_gust.py` with ualager's DockerHub password as argument. It build the docker image and publishes it to DockerHub repository. 

You should be able to see the published image `here <https://hub.docker.com/repository/docker/ualager/gust-lager/general>`__. You can follow the instructions in the Install and Usage section to verify the functionality of the deployed software. 

After you are done packaging and deploying, check :code:`git status`. If you bumped the version, :code:`src/build/settings/base.json` file will have changes in :code:`version` string. In main branch, just add, commit, and push the new change. You can also create a tag in github with description.

Adding more colors for vehicles
###############################

* Step 1
* Step 2




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`