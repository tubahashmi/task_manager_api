#!./venv/bin/python
# -*- coding: utf-8 -*-
"""Initializes schemas for all database collections required by Flask
resources."""
# First-party
from apiserver.api.schemas.roles import RoleSchema

__all__ = [
    'RoleSchema',
]