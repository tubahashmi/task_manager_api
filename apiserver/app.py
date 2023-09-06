#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Create Flask application and registers all views, extensions,
database connections, errors and exceptions.
"""

# Third-party
from flasgger import Swagger
from flask import Flask, jsonify, make_response
from werkzeug.exceptions import default_exceptions

# First-party
from apiserver import api, manage
from apiserver.commons.constants import APIResponse
from apiserver.extensions import db, jwt, migrate

__author__ = 'hashmiatna@gmail.com'


def create_app():
    """Application factory used to create application."""
    app = Flask('apiserver')
    app.config.from_object('apiserver.config')

    Swagger(app, config=configure_swagger(), merge=True)

    app.config.from_object('apiserver.config')

    configure_extensions(app)
    configure_cli(app)
    register_blueprints(app)
    register_errors(app)

    return app


def configure_swagger():
    """Swagger configurations"""

    return {
        'securityDefinitions': {
            'basicAuth': {'type': 'basic'},
            'authBearer': {
                # Workaround for Swagger 2.0 as it does not support
                # Bearer Token Authorization
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': '> - Enter the token with the `Bearer: ` prefix, '
                + 'e.g. "Bearer abcde12345".',
            },
        },
        'title': 'Task Management API Documentation',
        'version': '1.0',
        'termsOfService': None,
        'swagger_ui': True,
        'description': 'API documentation',
    }


def configure_extensions(app):
    """Configure Flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's CLI for easy entity management"""
    app.cli.add_command(manage.init)


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(api.views.blueprint)


def handle_exception(error):
    """Return JSON instead of HTML for HTTP errors"""
    response = {
        'status': APIResponse.ERROR.value,
        'message': error.name,
        'description': error.description,
        'code': error.code,
    }

    return make_response(jsonify(response), error.code)


def register_errors(app):
    """Register all errors and exceptions for application"""
    for ex in default_exceptions:
        app.register_error_handler(ex, handle_exception)
