import argparse


# %% setup and parse cmd line arguments
parser = argparse.ArgumentParser(description='Starts a local server to monitor for plugin data.')

parser.add_argument('port', type=int,
                    help='Port to listen on for incoming plugin data.')


args = parser.parse_args()


# %% create server on port


# %% main loop
while True:
    # if new packet exists:
        # read packet

        # determine database connection (plug name + id)

        # add data to database
    pass
