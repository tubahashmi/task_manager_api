#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Module containing unit tests for the CommentResource class.
"""
# pylint: disable=W0613,C0103,R0913


class TestCommentResource:
    """
    Test cases for the CommentResource class.
    """

    def test_get_comments_for_task(
        self, app, db, comment_resource, task_exists_mock, task_comments_mock
    ):
        """
        Test getting comments for a task with valid data.

        Args:
            app (Flask app): The Flask application context.
            db (Mock): Mocked database object.
            comment_resource (CommentResource): Instance of CommentResource for testing.
            task_exists_mock (MagicMock): Mocked Task.query.filter_by method.
            task_comments_mock (MagicMock): Mocked task.comments attribute.

        Test steps:
        1. Create a test request context with valid data.
        2. Make a GET request to retrieve comments for a task.
        3. Check the response status code and content.
        4. Assert that the response indicates success.
        """
        with app.test_request_context('/api/v1/tasks/1/comments', method='GET'):
            response = comment_resource.get(task_id=1)

            response_data = response[0]
            response_status = response[1]

            assert response_status.value == 200
            assert response_data['status'] == 'success'

    def test_get_comments_for_invalid_task(self, app, db, comment_resource):
        """
        Test getting comments for an invalid task.

        Args:
            app (Flask app): The Flask application context.
            db (Mock): Mocked database object.
            comment_resource (CommentResource): Instance of CommentResource for testing.

        Test steps:
        1. Create a test request context with an invalid task ID.
        2. Make a GET request to retrieve comments for a task.
        3. Check the response status code.
        4. Assert that the response status code indicates failure (404).
        """
        with app.test_request_context(
            '/api/v1/tasks/invalid_task_id/comments', method='GET'
        ):
            response = comment_resource.get(task_id='invalid_task_id')
            response_status = response[1]

            assert response_status.value == 404
