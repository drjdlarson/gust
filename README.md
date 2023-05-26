GUST
====

![gust_logo](https://github.com/drjdlarson/gust/assets/77820053/0d991c48-7aa3-46ff-84f1-f5d03a14ff9f)

The Ground Control Station (GCS) for Uncrewed Swarms and Teams (GUST) is an application developed by the Laboratory for Autonomy, GNC, and Estimation Research (LAGER) at The University of Alabama. GUST offers comprehensive planning, tracking, command, and control capabilities of an uncrewed swarm for teaming operations. It utilizes the standard MAVLink protocol to communicate with the swarm agents, enabling compatibility with various uncrewed autonomous systems such as Ardupilot based flight computers and Bolder Flight Systems. Full-stack development of GUST was done primarily based on PyQt5 framework. Its software architecture is designed to be modular for easy integration of external plugins and software packages. The GUST application runs inside a docker container making it compatible with any operating system with docker. It is also deployed on a ruggedized ground station box for LAGER’s outdoor survey and remote sensing operations with Uncrewed Aircraft Systems (UAS). 

Major Features:
- Capable of relaying real-time telemetry from all connected vehicles to a single Graphical User Interface (GUI) for convenient monitoring. 
- Easy integration of external plugins and tools.   
- Includes a Target tracking module with a GUI to configure and display real time tracking information from different sensors (example: ZED).  
- Includes a Planning module to design flight paths for individual vehicles or cooperative maneuvers for a swarm.  
- Provides ability for the ground station operator to command and control each vehicle for some specific tasks or during emergencies.  
- Storage of flight data from all vehicles for future analysis.  

DEV Setup
=========
Write about dev container setup.

Usage
=====
Write about deplyoment in hardware and installation process.

API Reference
=============
Put a link to the API reference. 
- Flowcharts.
- documentation from docstrings.
- Instructions on how to add maps, icons, colors.
- Instructions on using designer and converting to python. 
- Instructions on using Ardupilot SIL. 

Cite
====
Please cite the framework as follows

.. code-block:: bibtex

    @Misc{gncpy,
    author       = {Jordan D. Larson and Aabhash Bhandari and Ryan W. Thomas},
    howpublished = {Web page},
    title        = {{GUST}: A {G}round control station (GCS) for {U}ncrewed {S}warms and {T}eams},
    year         = {2022},
    url          = {https://github.com/drjdlarson/gust},
    }
..
