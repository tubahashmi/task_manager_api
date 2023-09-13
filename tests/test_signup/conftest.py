#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Module for defining fixtures for "SignupResource" unit tests.
"""
# pylint: disable=C0301,C0103
# Standard library
from unittest.mock import patch

# Third-party
import pytest

# First-party
from apiserver.api.resources import SignupResource
from tests.conftest import MockUser


@pytest.fixture
def signup_resource():
    """
    Fixture to create an instance of SignupResource for testing.
    """
    return SignupResource()


@pytest.fixture
def user_already_exists(app):
    """
    Fixture to patch User.query.filter_by to return an existing user.

    Args:
        app (Flask app): The Flask application context.

    Yields:
        MagicMock: A mock object for User.query.filter_by.
    """
    with app.test_request_context():
        user_query_mock = patch('apiserver.api.models.User.query')
        user_query_filter_by_mock = user_query_mock.start()

        # Modify the behavior to return an existing user when the email already exists
        user_query_filter_by_mock.return_value.first.return_value = MockUser(
            **{
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'password': 'hashed_password',  # Replace with the actual hashed password
            }
        )

        yield user_query_mock

    # Clean up the mock
    user_query_mock.stop()


@pytest.fixture
def db(app):
    """
    Fixture to patch the db object inside a Flask app.

    Args:
        app (Flask app): The Flask application context.

    Yields:
        MagicMock: A mock object for the 'db' object.
    """
    with app.test_request_context():
        db_mock = patch('apiserver.api.resources.users.db')
        db_mock_start = db_mock.start()

        yield db_mock_start

    # Clean up the mock
    db_mock.stop()
