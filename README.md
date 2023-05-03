# gust
GCS for Uncrewed Swarms and Teams (GUST)

# Setup
You should be able to pip install the gust package and get most of this, be sure to do that after pip installing the custom fork of fbs so the newer version of PyInstaller is used (may need the -U flag when installing gust). You will need to manually install pyqt5-tools. Otherwise, this requires

- python 3.7
- PyQt5
- PyQt5-tools
- flask
- flask-restx
- requests
- gunicorn (linux/mac) and/or waitress (windows)

 This should all work in either a virtual environment or a conda environment (everything installed with pip). For freezing (packaging) and creating installer files a custom fork of fbs is required (TODO: setup actual fork and link it here).

# Converting UI files
A helper script `convert_ui_files.py` has been included to automatically convert all \*.ui files to \*.py files. This assumes that pyuic5 is installed and the \*.ui files are in the standard location.

# Helpful commands
To get the qt designer run `qt5-tools designer`

# Docker Compose
See <https://www.stereolabs.com/docs/docker/building-arm-container-on-x86/> for multi-arch containers
and <https://github.com/tldr-pages/tldr/blob/master/pages/common/docker-compose.md> for docker-compose commands

The **lager_sensors** repo must be cloned inside gust at the root level for the docker containers, this is because the repo is private and this is easier than dealing with ssh keys in the conatainers.

Install QEMU for hardware emulation with `sudo apt-get install qemu binfmt-support qemu-user-static`

Run `docker run --rm --privileged multiarch/qemu-user-static --reset -p yes` to activate the emulation (should only need to be done once?).

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
    
