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

    def test_update_comment_with_valid_data(  #   pylint: disable=R0913
        self, app, db, comment_resource, task_exists_mock, comment_exists_mock
    ):
        """
        Test updating a comment with valid data.

        Args:
            app (Flask app): The Flask application context.
            db (Mock): Mocked database object.
            comment_resource (CommentResource): Instance of CommentResource for testing.
            task_exists_mock (MagicMock): Mocked Task.query.filter_by method.
            comment_exists_mock (MagicMock): Mocked Comment.query.filter_by method.

        Test steps:
        1. Create a test request context with valid data.
        2. Make a PUT request to update a comment.
        3. Check the response status code and content.
        4. Assert that the response indicates success.
        """
        data = {'comment': 'Updated comment content.'}
        with app.test_request_context(
            '/api/v1/tasks/123abc/comments/456def',
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
        ):
            response = comment_resource.put(task_id='123abc', comment_id='456def')

        response_data = response[0]
        response_status = response[1]

        assert response_status.value == 200
        assert response_data['status'] == 'success'

    def test_update_comment_with_invalid_task(self, app, db, comment_resource):
        """
        Test updating a comment with an invalid task.

        Args:
            app (Flask app): The Flask application context.
            db (Mock): Mocked database object.
            comment_resource (CommentResource): Instance of CommentResource for testing.

        Test steps:
        1. Create a test request context with an invalid task ID.
        2. Make a PUT request to update a comment.
        3. Check the response status code and content.
        4. Assert that the response indicates failure.
        """
        data = {'comment': 'Updated comment content.'}
        with app.test_request_context(
            '/api/v1/tasks/invalid_task_id/comments/456def',
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
        ):
            response = comment_resource.put(
                task_id='invalid_task_id', comment_id='456def'
            )

        response_data = response[0]
        response_status = response[1]

        assert response_status.value == 404
        assert response_data['status'] == 'failed'

    def test_update_comment_with_invalid_comment(self, app, db, comment_resource):
        """
        Test updating a comment with an invalid comment.

        Args:
            app (Flask app): The Flask application context.
            db (Mock): Mocked database object.
            comment_resource (CommentResource): Instance of CommentResource for testing.

        Test steps:
        1. Create a test request context with an invalid comment ID.
        2. Make a PUT request to update a comment.
        3. Check the response status code and content.
        4. Assert that the response indicates failure.
        """
        data = {'comment': 'Updated comment content.'}
        with app.test_request_context(
            '/api/v1/tasks/123abc/comments/invalid_comment_id',
            method='PUT',
            data=json.dumps(data),
            content_type='application/json',
        ):
            response = comment_resource.put(
                task_id='123abc', comment_id='invalid_comment_id'
            )

        response_data = response[0]
        response_status = response[1]

        assert response_status.value == 404
        assert response_data['status'] == 'failed'
