#!/bin/bash

echo "Running the entrypoint script..."

# installing the zed and fbs packages
pip install /workspaces/gust/repos/fbs/
pip install /workspaces/gust/repos/lager_sensors/zed/

# installing the packages
pip install /workspaces/gust/utilities/
pip install /workspaces/gust/gust_packages/wsgi_apps/
pip install /workspaces/gust/gust_packages/radio_manager/

# overriding what fbs installs
pip install pyinstaller==4.9

# clear all the outputs from above scripts
clear

# leave the terminal open
/bin/bash
