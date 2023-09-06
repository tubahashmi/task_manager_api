#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Initializes all models."""

# First-party
from apiserver.api.models.roles import Role
from apiserver.api.models.users import User
from apiserver.api.models.tasks import Task, Comment

__all__ = [
    'Role',
    'User',
    'Comment',
    'Task'
]
