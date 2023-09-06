#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Register API views."""

# Third-party
from flask import Blueprint
from flask_restful import Api

# First-party
from apiserver.api.resources import (
    DeleteAccount,
    SigninResource,
    SignupResource,
    UserResource,
    UsersListResource,
)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(SigninResource, '/sign_in', endpoint='sign_in')
api.add_resource(SignupResource, '/sign_up', endpoint='sign_up')
api.add_resource(UserResource, '/user_info', endpoint='user_info')
api.add_resource(UsersListResource, '/users', endpoint='list_users')
api.add_resource(DeleteAccount, '/delete_user/<string:user_id>', endpoint='delete_user')
