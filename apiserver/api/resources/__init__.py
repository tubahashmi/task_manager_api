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

__all__ = [
    'DeleteAccount',
    'UserResource',
    'UsersListResource',
    'SigninResource',
    'SignupResource',
]
