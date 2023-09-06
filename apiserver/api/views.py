#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Register API views."""

# Third-party
from flask import Blueprint
from flask_restful import Api

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)
