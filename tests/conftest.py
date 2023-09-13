#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Module containing mock classes and fixtures for unit tests.
"""
# pylint: disable=C0103,W0621


# Third-party
import pytest

# First-party
from apiserver.app import create_app
from tests.config import TestingConfig


class MockTask:
    """A mock class for representing a task."""

    def __init__(self, **kwargs):
        """Initialize a MockTask instance with the given keyword arguments."""
        self.__dict__.update(kwargs)


class MockComment:
    """A mock class for representing a comment."""

    def __init__(self, **kwargs):
        """Initialize a MockComment instance with the given keyword arguments."""
        self.__dict__.update(kwargs)


class MockRole:
    """A mock class for representing a role."""

    def __init__(self, _id=1):
        """Initialize a MockRole instance with an optional 'id' parameter."""
        self.id = _id


class MockUser:
    """A mock class for representing a user."""

    def __init__(self, **kwargs):
        """Initialize a MockUser instance with the given keyword arguments."""
        self.__dict__.update(kwargs)


@pytest.fixture
def app():
    """Fixture for creating a Flask test app.

    This fixture sets up a Flask test app with testing configuration.

    Yields:
        Flask app: The Flask test app.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = None
    app.config.from_object(TestingConfig)
    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()
