#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Module containing configuration classes for the application.

This module defines two configuration classes, `Config` and `TestingConfig`,
used to configure various aspects of the application.

Attributes:
    - `Config`: Base configuration class for the application.
    - `TestingConfig`: Configuration class for testing, extending
            the base configuration.

Both classes provide attributes for configuring the application's behavior,
including database connection settings and debugging options.
"""

# Standard library
import os


class Config:
    """
    Base configuration class for the application.

    Attributes:
        DEBUG (bool): Set to False for production, True for development.
        TESTING (bool): Set to False for production, True for testing.
        SQLALCHEMY_DATABASE_URI (str): The URI for the database connection.
            Defaults to 'mysql:///' if DATABASE_URI environment variable is not set.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Set False to
            disable tracking modifications.
    """

    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI') or 'mysql:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """
    Configuration class for testing, extending the base configuration.

    Attributes:
        DEBUG (bool): Set to True for testing.
        SQLALCHEMY_DATABASE_URI (None): Database URI is set to None for testing
            to allow patching the database.
        TESTING (bool): Set to True for testing.
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = None  # patch the database instead
    TESTING = True
