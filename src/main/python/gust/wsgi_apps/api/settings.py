"""Define settings and configuration values for the app."""
import os

basedir = os.path.abspath(os.path.dirname(__file__))

ENV = 'development'
ENV_KEY = 'LAGER_GUST_API_ENV'

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "test.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "prod.sqlite")


env_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
