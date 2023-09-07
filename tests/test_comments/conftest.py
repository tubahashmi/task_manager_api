from unittest.mock import patch

import pytest

from apiserver.api.resources import CommentResource


# Create a TaskResource instance for testing
@pytest.fixture
def comment_resource():
    return CommentResource()


class MockTask:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class MockComment:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


# Mock the Task.query.filter_by method to return a task
@pytest.fixture
def task_exists_mock(app):
    with app.app_context():
        task_query_mock = patch('apiserver.api.models.Task.query')
        task_query_filter_by_mock = task_query_mock.start()
        task_query_filter_by_mock.return_value.first.return_value = MockTask(**{
            'id': 1,
            'title': 'mock task'
        })
        yield task_query_mock
    task_query_mock.stop()

# Mock the Comment.query.filter_by method to return a comment
@pytest.fixture
def comment_exists_mock(app):
    with app.app_context():
        comment_query_mock = patch('apiserver.api.models.Comment.query')
        comment_query_filter_by_mock = comment_query_mock.start()
        comment_query_filter_by_mock.return_value.first.return_value = MockComment(**{
            'id': 1,
        })
        yield comment_query_mock
        comment_query_mock.stop()


# Mock the task.comments attribute to return a list of comments
@pytest.fixture
def task_comments_mock(app):
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
    """Patch db object inside flask app"""
    with app.test_request_context():
        db_mock = patch('apiserver.api.resources.tasks.db')
        db_mock_start = db_mock.start()

        yield db_mock_start

    # Clean up the mock
    db_mock.stop()