#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Module for defining fixtures for "CommentResource" unit tests.
"""
# pylint: disable=C0103

# Standard library
from unittest.mock import patch

# Third-party
import pytest

# First-party
from apiserver.api.resources import CommentResource
from tests.conftest import MockComment, MockTask


@pytest.fixture
def comment_resource():
    """
    Fixture to create a CommentResource instance for testing.
    """
    return CommentResource()


@pytest.fixture
def task_exists_mock(app):
    """
    Fixture to mock the Task.query.filter_by method to return a task.

    Args:
        app (Flask app): The Flask application context.

    Yields:
        MagicMock: A mock object for Task.query.
    """
    with app.app_context():
        task_query_mock = patch('apiserver.api.models.Task.query')
        task_query_filter_by_mock = task_query_mock.start()
        task_query_filter_by_mock.return_value.first.return_value = MockTask(
            **{'id': 1, 'title': 'mock task'}
        )
        yield task_query_mock
    task_query_mock.stop()


@pytest.fixture
def comment_exists_mock(app):
    """
    Fixture to mock the Comment.query.filter_by method to return a comment.

    Args:
        app (Flask app): The Flask application context.

    Yields:
        MagicMock: A mock object for Comment.query.
    """
    with app.app_context():
        comment_query_mock = patch('apiserver.api.models.Comment.query')
        comment_query_filter_by_mock = comment_query_mock.start()
        comment_query_filter_by_mock.return_value.first.return_value = MockComment(
            **{
                'id': 1,
            }
        )
        yield comment_query_mock
    comment_query_mock.stop()


@pytest.fixture
def task_comments_mock(app):
    """
    Fixture to mock the task.comments attribute to return a list of comments.

    Args:
        app (Flask app): The Flask application context.

    Yields:
        MagicMock: A mock object for Task.query.
    """
    with app.app_context():
        task = MockTask(id='123abc')
        comment1 = MockComment(id='comment1', content='Comment 1')
        comment2 = MockComment(id='comment2', content='Comment 2')
        task.comments = [comment1, comment2]

        task_query_mock = patch('apiserver.api.models.Task.query')
        task_query_filter_mock = task_query_mock.start()
        task_query_filter_mock.return_value.first.return_value = task

        yield task_query_mock
    task_query_mock.stop()


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
        db_mock = patch('apiserver.api.resources.tasks.db')
        db_mock_start = db_mock.start()
        yield db_mock_start
    db_mock.stop()
