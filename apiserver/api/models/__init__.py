#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Initializes all models."""

# First-party
from apiserver.api.models.roles import Role
from apiserver.api.models.users import User

__all__ = [
    'Role',
    'User',
]
