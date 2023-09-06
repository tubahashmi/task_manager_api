#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Initializes all required Flask-RESTful resources.
"""

from apiserver.api.resources.users import DeleteAccount, UserResource, UsersListResource, SignupResource, SigninResource

__all__ = [
    'DeleteAccount',
    'UserResource',
    'UsersListResource',
    'SigninResource',
    'SignupResource'
]
