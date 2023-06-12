#!/bin/bash

echo "running the entrypoint script..."
mkdir testing_dir

# installing the zed and fbs packages
pip install gust/repos/fbs/
pip install gust/repos/lager_sensors/zed/

# installing the packages
pip install gust/utilities/
pip install gust/gust_packages/wsgi_apps/
pip install gust/gust_packages/radio_manager/

# overriding what fbs installs
pip install pyinstaller==4.9

# exec "$@"
/bin/bash