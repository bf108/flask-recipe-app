import os
from os import path, environ
from dotenv import load_dotenv
from datetime import timedelta

BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, '.env'))

class Config:
    """Base config."""
    FLASK_APP = os.path.join(BASEDIR, 'runner.py')
    SECRET_KEY = environ.get('SECRET_KEY')
    SESSION_COOKIE_NAME = environ.get('SESSION_COOKIE_NAME')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL',
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'app.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    # PORT = 5002

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    # DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    # DATABASE_URI = environ.get('DEV_DATABASE_URI')

class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    #This allows you to run CRUD commands against a test db instead of prod or dev one
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI',
                                        default=f"sqlite:///{os.path.join(BASEDIR, 'instance', 'test.db')}")

    