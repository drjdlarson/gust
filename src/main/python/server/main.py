"""Main entry point of the Server/Data recorder function."""
import argparse
import subprocess
import os

from api.config import env_config


# %% Main Entry Point
if __name__ == "__main__":
    # %%% Setup Input Arguments
    parser = argparse.ArgumentParser(description='Start the ground station backend.')

    env = "development"
    msg = 'Environment to run the server in. The default is {:s}'.format(env)
    parser.add_argument('--env', type=str, help=msg, default=env,
                        choices=env_config.keys())

    port = 8000
    msg = 'Port number to listen on. The default is {:d}'.format(port)
    parser.add_argument('--port', '-p',
                        help=msg, default=port, type=int)

    num_workers = 1
    msg = ('Number of worker threads to start for the server. '
           + 'The default is {:d}'.format(num_workers))
    parser.add_argument('--num-workers', help=msg, default=num_workers,
                        type=int)

    # %% Process input arguments
    args = parser.parse_args()

    env = args.env
    port = args.port
    num_workers = args.num_workers

    # %%% Startup web server
    os.environ["LAGER_GUST_ENV"] = env

    # TODO: figure out what to do with stdout/err of subproc
    # TODO: figure out if need to avoid zombies
    server_proc = subprocess.Popen(['gunicorn',
                                    '-b 127.0.0.1:{:d}'.format(port),
                                    '-w {:d}'.format(num_workers),
                                    'wsgi:app'])

    # %%% Startup sensor reading (in subprocesses?)

    # %%% Main event loop
    while 1:
        # listen for events from sensors for new data
            # write data to data base

        pass
