#!/bin/bash

# python -m pip install ~/workspaces/gust/repos/fbs/
python -m pip install gust/repos/lager_sensors/zed/
mkdir some_test
echo "Entrypoint bash script is running"

echo "............................"
exec "$@"

# /bin/bash




