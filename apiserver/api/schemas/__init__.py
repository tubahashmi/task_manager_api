#!./venv/bin/python
# -*- coding: utf-8 -*-
"""Initializes schemas for all database collections required by Flask
resources."""
# pylint: disable=R0401

# First-party

from apiserver.api.schemas.roles import RoleSchema
from apiserver.api.schemas.users import UserSchema

__all__ = ['RoleSchema', 'UserSchema']
