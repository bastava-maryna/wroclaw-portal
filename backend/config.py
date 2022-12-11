"""database configuration file"""

from os import environ, path
from dotenv import load_dotenv
from datetime import timedelta

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))


class Config:
    """base config"""

    SECRET_KEY = environ.get("SECRET_KEY")
    SQL_ALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_MIGRATE_REPO = path.join(basedir, "db_repository")

    CORS_HEADERS = "Content-Type"

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(environ.get("JWT_ACCESS_TOKEN_EXPIRES"))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(environ.get("JWT_REFRESH_TOKEN_EXPIRES"))
    )

    SWAGGER_URL = "/api/docs"


class ProdConfig(Config):
    """production specific configuration"""

    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = environ.get("PROD_DATABASE_URI")
    SQLALCHEMY_BINDS = {"docs_db": environ.get("PROD_DOCS_DATABASE_URI")}
    # API_URL=''


class DevConfig(Config):
    """development specific configuration"""

    FLASK_ENV = "development"
    # DEBUG = True
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = environ.get("DEV_DATABASE_URI")
    # SQLALCHEMY_BINDS = {"docs_db": environ.get("DEV_DOCS_DATABASE_URI")}
    print("dev============================" + SQLALCHEMY_DATABASE_URI)
    API_URL = "/swagger.yaml"
    # API_URL = "/backend/swagger.yaml"
    # API_URL = path.join(basedir, "/swagger.yaml")
