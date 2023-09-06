#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Define class for role collection in db."""

# pylint: disable=E1101

# Third-party
from sqlalchemy.orm import relationship

# First-party
from apiserver.extensions import db


class Role(db.Model):
    """
    Represents user roles in the system.

    Attributes:
        id (int): A unique identifier for the role.
        name (str): The name of the role (e.g., 'admin', 'user').
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=None)
    name = db.Column(db.String(20), unique=True, nullable=False)

    users = relationship('User', back_populates='role')

    def __init__(self, name):
        """
        Initialize a new Role instance.

        Args:
            name (str): The name of the role.
        """
        self.name = name
