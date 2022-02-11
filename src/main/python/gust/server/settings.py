"""Main entry point of the Server/Data recorder function."""

# %% Web server startup
PORT = 8000
ENV = 'development'
ENV_KEY = 'LAGER_GUST_ENV'
NUM_WORKERS = 1
DAEMON = False


# %% Main Entry Point
if __name__ == "__main__":
    # %%% Setup Input Arguments

    # %%% Startup web server


    # %%% Startup sensor reading (in subprocesses?)

    # %%% Main event loop
    while 1:
        # listen for events from sensors for new data
            # write data to data base

        pass
