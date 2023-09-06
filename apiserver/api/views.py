#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Register API views."""

# Third-party
from flask import Blueprint
from flask_restful import Api

# First-party
from apiserver.api.resources import (
    AssignedTasksListResource,
    AssignTaskResource,
    CommentResource,
    DeleteAccount,
    SigninResource,
    SignupResource,
    TaskResource,
    UserResource,
    UsersListResource,
)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

resource_config = {
    SigninResource: [
        {
            'endpoint': '/sign_in',
            'methods': ['POST'],
        },
    ],
    SignupResource: [
        {
            'endpoint': '/sign_up',
            'methods': ['POST'],
        },
    ],
    UserResource: [
        {
            'endpoint': '/user_info',
            'methods': ['GET'],
        },
    ],
    UsersListResource: [
        {
            'endpoint': '/users',
            'methods': ['GET'],
        },
    ],
    DeleteAccount: [
        {
            'endpoint': '/delete_user/<string:user_id>',
            'methods': ['DELETE'],
        },
    ],
    TaskResource: [
        {
            'endpoint': '/tasks/<string:task_id>',
            'methods': ['PUT', 'DELETE'],
        },
        {
            'endpoint': '/tasks/add',
            'methods': ['POST'],
        },
        {
            'endpoint': '/tasks',
            'methods': ['GET'],
        },
    ],
    AssignedTasksListResource: [
        {
            'endpoint': '/assigned-tasks-list',
            'methods': ['GET'],
        },
    ],
    AssignTaskResource: [
        {
            'endpoint': '/assign-task',
            'methods': ['POST'],
        },
    ],
    CommentResource: [
        {
            'endpoint': '/tasks/<string:task_id>/comments',
            'methods': ['POST', 'GET'],
        },
        {
            'endpoint': '/tasks/<string:task_id>/comments/<int:comment_id>',
            'methods': ['PUT', 'DELETE'],
        },
    ],
}

for resource_class, methods_config in resource_config.items():
    for method_info in methods_config:
        api.add_resource(
            resource_class,
            method_info['endpoint'],
            endpoint=method_info['endpoint'].replace(
                '/', '_'
            ),  # Use endpoint as 'resource_method'
            methods=method_info['methods'],
        )
