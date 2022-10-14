# gust
GCS for Unmanned Swarms and Teams (GUST)

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
