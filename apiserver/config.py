#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Default configuration.

Use environment variables to override.
"""

# Standard library
import os

# FLASK
DEBUG = ENV = os.getenv('FLASK_ENV')

# DATABASE
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DB = os.getenv('MYSQL_DB')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI').format(
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    db=MYSQL_DB,
)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# BASIC AUTHORIZATION
BASIC_AUTHORIZATION = os.getenv('BASIC_AUTHORIZATION')
BASIC_AUTH_USERNAME = os.getenv('BASIC_AUTH_USERNAME')
BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
