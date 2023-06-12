#!/bin/bash

echo "running the entrypoint script..."
mkdir testing_dir

# installing the zed and fbs packages
pip install /workspaces/gust/repos/fbs/
pip install /workspaces/gust/repos/lager_sensors/zed/

# installing the packages
pip install /workspaces/gust/utilities/
pip install /workspaces/gust/gust_packages/wsgi_apps/
pip install /workspaces/gust/gust_packages/radio_manager/

# overriding what fbs installs
pip install pyinstaller==4.9

exec "$@"
# /bin/bash