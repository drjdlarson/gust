# gust
GCS for UAS Swarming and Teaming (GUST)

# Setup
This requires

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
