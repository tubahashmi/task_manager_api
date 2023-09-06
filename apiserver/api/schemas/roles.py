#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Define Schema for Role."""

# Third-party
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# First-party
from apiserver.api.models.roles import Role


class RoleSchema(SQLAlchemyAutoSchema):
    """Defines schema for Role collection."""

    class Meta:
        """Metadata about Role table."""

        model = Role
