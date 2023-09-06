#!./venv/bin/python
# -*- coding: utf-8 -*-
"""
Utilities functions
"""
# Standard library
import re

from flask import jsonify, make_response
# Third-party
from sqlalchemy.exc import SQLAlchemyError

# First-party
from apiserver.api.models import User


def is_valid_email(email):
    """Defines a regular expression pattern for a valid email address"""
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Use the re.match() function to check if the email matches the pattern
    if re.match(email_pattern, email):
        return True
    return False


def authenticate_user(username, password):
    """Validate user's credentials"""
    try:
        user = User.query.filter_by(email=username).first()
        if user and user.check_password(password):
            return user
    except SQLAlchemyError:
        return None
    return None


def custom_unauthorized():
    return make_response(
        jsonify({"message": "Authentication failed. Invalid credentials"}), 401
    )