#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Initializes all required Flask-RESTful resources.
"""

# First-party
from apiserver.api.resources.users import (
    DeleteAccount,
    SigninResource,
    SignupResource,
    UserResource,
    UsersListResource,
)
from apiserver.api.resources.tasks import (
TaskResource, AssignedTasksListResource, CommentResource, AssignTaskResource
)

__all__ = [
    'DeleteAccount',
    'UserResource',
    'UsersListResource',
    'SigninResource',
    'SignupResource',
    'TaskResource',
    'AssignedTasksListResource',
    'CommentResource',
    'AssignTaskResource'
]
