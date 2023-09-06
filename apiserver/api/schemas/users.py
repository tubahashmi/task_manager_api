#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Define Schema for User."""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apiserver.api.models.users import User
from apiserver.api.schemas import RoleSchema
from apiserver.extensions import db, ma


class UserSchema(SQLAlchemyAutoSchema):
    """Defines schema for user collection."""
    class Meta:
        """Metadata about user table."""
        model = User
        sqla_session = db.session
        load_instance = True
        exclude = ('password',)

    id = ma.String(data_key='id')
    email = ma.String(data_key='email')
    first_name = ma.String(data_key='firstName')
    last_name = ma.String(data_key='lastName')
    created_at = ma.DateTime(data_key='createdAt')
    role = ma.Nested(RoleSchema, data_key='role', only=['name'])