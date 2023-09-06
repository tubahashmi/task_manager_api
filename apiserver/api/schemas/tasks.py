#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Define Schema for Task and Comment."""
# pylint: disable=E1101

# Third-party
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

# First-party
from apiserver.api.models import Comment, Task
from apiserver.api.schemas import UserSchema
from apiserver.extensions import db, ma


class TaskSchema(SQLAlchemyAutoSchema):
    """Defines schema for task collection."""

    class Meta:
        """Metadata about task table."""

        model = Task
        sqla_session = db.session
        load_instance = True

    id = ma.String(data_key='id')
    title = ma.String(data_key='title')
    description = ma.String(data_key='description')
    due_date = ma.DateTime(data_key='dueDate')
    priority = ma.String(data_key='priority')
    status = ma.String(data_key='status')
    created_by = ma.Nested(UserSchema, data_key='createdBy', only=['id', 'email'])
    assigned_to = ma.Nested(UserSchema, data_key='assignedTo', only=['id', 'email'])
    created_at = ma.DateTime(data_key='createdAt')
    updated_at = ma.DateTime(data_key='updatedAt')
    completion_date = ma.DateTime(data_key='completionDate')
    tags = ma.String(data_key='tags')
    recurring_task = ma.Boolean(data_key='recurringTask')
    estimate = ma.Integer(data_key='estimate')
    actual_time_spent = ma.Integer(data_key='actualTimeSpent')

    # Custom fields to enforce conversion
    type = ma.Function(lambda obj: obj.type.value)
    priority = ma.Function(lambda obj: obj.priority.value)
    status = ma.Function(lambda obj: obj.status.value)


class CommentSchema(SQLAlchemyAutoSchema):
    """Defines schema for comment collection."""

    class Meta:
        """Metadata about comment table."""

        model = Comment
        sqla_session = db.session
        load_instance = True

    id = ma.String(data_key='id')
    content = ma.String(data_key='content')
    created_at = ma.DateTime(data_key='createdAt')
