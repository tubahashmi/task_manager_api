import os


class Config:
    """
    Defines Config
    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or 'mysql:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """
    Extends Config for Test
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = None  # patch database instead
    TESTING = True
