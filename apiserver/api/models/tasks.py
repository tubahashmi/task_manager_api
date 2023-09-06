#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Define class for task record."""
import uuid
# pylint: disable=E1101

# Standard library
from datetime import datetime

from sqlalchemy import ForeignKeyConstraint

# First-party
from apiserver.commons.constants import PriorityLevel, TaskStatus, TASK_DATETIME_DEFAULT, TASKS_ID, \
    TaskType
from apiserver.extensions import db


class Task(db.Model):
    """
    Represents a task in the system.

    Attributes:
        id (str): A unique UUID for the task.
        created_at (datetime): Timestamp of when the task record was created.
    """

    __tablename__ = 'tasks'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    title = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.Enum(PriorityLevel), nullable=False, default=PriorityLevel.MEDIUM)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.OPEN)
    created_by_id = db.Column(db.Integer,
                              db.ForeignKey('users.id'))  # Relationship with the 'User' who created the task
    created_by = db.relationship('User', backref='tasks_created', foreign_keys=[created_by_id])
    assigned_to_id = db.Column(db.Integer,
                               db.ForeignKey('users.id'))  # Relationship with the 'User' assigned to the task
    assigned_to = db.relationship('User', backref='tasks_assigned', foreign_keys=[assigned_to_id])
    created_at = db.Column(db.DateTime, default=TASK_DATETIME_DEFAULT)
    updated_at = db.Column(db.DateTime, default=TASK_DATETIME_DEFAULT)
    completion_date = db.Column(db.DateTime, nullable=True)
    recurring_task = db.Column(db.Boolean, default=False)
    estimate = db.Column(db.Integer, nullable=True)
    actual_time_spent = db.Column(db.Integer, nullable=True)
    comments = db.relationship('Comment', backref='task', cascade='all, delete-orphan')
    type = db.Column(db.Enum(TaskType), nullable=False, default=TaskType.TASK)


class Comment(db.Model):
    """
    Represents a comment on a task.

    Attributes:
        id (int): A unique identifier for the comment.
        content (str): The content of the comment.
        created_at (datetime): Timestamp of when the comment was created.
        task_id (int): The ID of the task to which the comment belongs.
    """

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=TASK_DATETIME_DEFAULT)
    task_id = db.Column(db.Integer, db.ForeignKey(TASKS_ID), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        }