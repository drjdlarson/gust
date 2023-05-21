"""Main file running the WSGI application"""
import logging
import gunicorn.app.base
import gunicorn.glogging as glogging

from argparse import ArgumentParser

# from wsgi_apps import logger
from wsgi_apps.api import app as api_app


# see https://stackoverflow.com/questions/41087790/how-to-override-gunicorns-logging-config-to-use-a-custom-formatter
class CustomLogger(glogging.Logger):
    """Custom logger for Gunicorn log messages."""

    def setup(self, cfg):
        """Configure Gunicorn application logging configuration."""
        super().setup(cfg)

        # Override Gunicorn's `error_log` configuration.
        self._set_handler(
            self.error_log,
            cfg.errorlog,
            logging.Formatter("[wsgi-app] %(levelname)s %(asctime)s - %(message)s"),
        )


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)
        self.cfg.set('logger_class', CustomLogger)

    def load(self):
        return self.application


def define_parser():
    parser = ArgumentParser(
        description="Process command line options for the WSGI apps."
    )

    # parser.add_argument("database_path", type=str, help="Path to the database file")

    default = "8000"
    parser.add_argument(
        "--port",
        type=str,
        help="Port for the gunicorn server. The default is {}".format(default),
        default=default,
    )

    default = "127.0.0.1"
    parser.add_argument(
        "--ip",
        type=str,
        help="IP for the gunicorn server. The default is {}".format(default),
        default=default,
    )

    default = 1
    parser.add_argument(
        "--num-workers",
        type=int,
        help="Number of workers for the gunicorn server. The default is {}".format(
            default
        ),
        default=default,
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Run in debug mode",
    )

    return parser


if __name__ == "__main__":
    args = define_parser().parse_args()

    gunicorn_logger = logging.getLogger("gunicorn.error")

    options = {
        "bind": "%s:%s" % (args.ip, args.port),
        "workers": args.num_workers,
    }

    StandaloneApplication(api_app.create_app(), options).run()
