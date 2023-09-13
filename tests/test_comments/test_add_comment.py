#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Module containing unit tests for the CommentResource class.
"""
#   pylint: disable=W0613,C0103,C0301

# Standard library
import json


class TestCommentResource:
    """
    Test cases for the CommentResource class.
    """

    def test_create_comment_with_valid_data(
        self, app, db, comment_resource, task_exists_mock
    ):  # pylint: disable=C0103
        """
        Test creating a comment with valid data.

        Args:
            app (Flask app): The Flask application context.
            db (Mock): Mocked database object.
            comment_resource (CommentResource): Instance of CommentResource for testing.
            task_exists_mock (MagicMock): Mocked Task.query.filter_by method.

        Test steps:
        1. Create a test request context with valid data.
        2. Make a POST request to create a comment.
        3. Check the response status code and content.
        4. Assert that the response indicates success.
        """

        data = {'comment': 'This is a test comment.'}
        with app.test_request_context(
            '/api/v1/tasks/1/comments',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
        ):
            response = comment_resource.post(task_id=1)

        response_data = response[0]
        response_status = response[1]

        assert response_status.value == 201
        assert response_data['status'] == 'success'

    def test_create_comment_with_invalid_task(
        self, app, db, comment_resource
    ):  # pylint: disable=C0103
        """
        Test creating a comment with an invalid task.

        Args:
            app (Flask app): The Flask application context.
            db (Mock): Mocked database object.
            comment_resource (CommentResource): Instance of CommentResource for testing.

        Test steps:
        1. Create a test request context with invalid task ID.
        2. Make a POST request to create a comment.
        3. Check the response status code and content.
        4. Assert that the response indicates failure.
        """
        data = {'comment': 'This is a test comment.'}
        with app.test_request_context(
            '/api/v1/tasks/invalid_task_id/comments',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
        ):
            response = comment_resource.post(task_id='invalid_task_id')

        response_data = response[0]
        response_status = response[1]

        assert response_status.value == 404
        assert response_data['status'] == 'failed'
