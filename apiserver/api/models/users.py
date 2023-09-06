#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Define class for user record."""

# pylint: disable=E1101

# Standard library
from datetime import datetime

# Third-party
from werkzeug.security import check_password_hash, generate_password_hash

# First-party
from apiserver.commons.constants import TASK_UUID_DEFAULT, TASK_DATETIME_DEFAULT
from apiserver.extensions import db


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (str): A unique UUID for the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user (unique).
        password (str): Hashed password of the user.
        role_id (int): Foreign key to associate a user with a role.
        created_at (datetime): Timestamp of when the user record was created.

    Relationships:
        role (Role): Defines the many-to-one relationship between User and Role.
    """

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        nullable=False,
    )
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=TASK_DATETIME_DEFAULT)

    # Define the many-to-one relationship between User and Role
    role = db.relationship('Role', foreign_keys=[role_id], back_populates='users')

    def set_password(self, password):
        """
        Hash and set the user's password.

        Args:
            password (str): The plain text password to hash and store.
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the provided password matches the stored hashed password.

        Args:
            password (str): The plain text password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password, password)
