#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Extensions registry.

All extensions here are used as singletons and initialized in
application factory.
"""

# Third-party
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# First-party
from apiserver.commons.logging import Logger

basic_auth = HTTPBasicAuth()
db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
logger = Logger()
