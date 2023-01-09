import logging
import gunicorn.app.base
from argparse import ArgumentParser

from wsgi_apps import logger
from wsgi_apps.api import app as api_app


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def define_parser():
    parser = ArgumentParser(description="Process command line options for the WSGI apps.")

    # parser.add_argument("database_path", type=str, help="Path to the database file")

    default = "8000"
    parser.add_argument(
        "--port",
        type=str,
        help="Port for the gunicorn server. The default is {}".format(default),
        default=default
    )

    default = "127.0.0.1"
    parser.add_argument(
        "--ip",
        type=str,
        help="IP for the gunicorn server. The default is {}".format(default),
        default=default
    )

    default = 1
    parser.add_argument(
        "--num-workers",
        type=int,
        help="Number of workers for the gunicorn server. The default is {}".format(default),
        default=default
    )

    parser.add_argument(
        "-d", "--debug",
        action="store_true",
        help="Run in debug mode",
    )

    return parser


if __name__ == '__main__':
    args = define_parser().parse_args()

    ch = logging.StreamHandler()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)

    formatter = logging.Formatter('[wsgi-app] %(levelname)s %(asctime)s - %(message)s')
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    # see https://stackoverflow.com/questions/53548536/how-to-use-the-logging-module-in-python-with-gunicorn
    # and https://docs.gunicorn.org/en/stable/settings.html#logconfig for a cleaner way with config files that can be passed where we start the process
    gunicorn_logger = logging.getLogger('gunicorn.glogging.Logger')
    gunicorn_logger.handlers = logger.handlers
    gunicorn_logger.setLevel(logger.level)

    options = {
        'bind': '%s:%s' % (args.ip, args.port),
        'workers': args.num_workers,
    }

    StandaloneApplication(api_app.create_app(logger_override=logger), options).run()
