#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Module containing unit tests for the SigninResource class.
"""
#   pylint: disable=W0613,C0103,C0301,W0611

# Standard library
import json
from unittest.mock import patch

# First-party
from apiserver.api.models import User


class TestSigninResource:
    """
    Test cases for the SigninResource class.
    """

    def test_successful_user_login(
        self, app, signin_resource, user_authentication_success_mock
    ):
        """
        Test successful user login.

        Args:
            app (Flask app): The Flask application context.
            signin_resource (SigninResource): Instance of SigninResource for testing.
            user_authentication_success_mock (MagicMock): Mocked user authentication for success.

        Test steps:
        1. Create a test request context with valid login data.
        2. Make a POST request to simulate a successful login.
        3. Check the response status code and content.
        4. Assert that the response indicates success.
        """
        # Call the post method to simulate a successful login
        with app.test_request_context('/api/v1/sign_in', method='POST'):
            response = signin_resource.post()

            # Assert the response for success
            assert response[1] == 200
            assert 'access_token' in response[0]
            assert response[0]['status'] == 'success'

    def test_user_login_failure(
        self, app, signin_resource, user_authentication_failure_mock
    ):
        """
        Test user login failure with incorrect password.

        Args:
            app (Flask app): The Flask application context.
            signin_resource (SigninResource): Instance of SigninResource for testing.
            user_authentication_failure_mock (MagicMock): Mocked user authentication for failure.

        Test steps:
        1. Create invalid login data with an incorrect password.
        2. Create a test request context with the invalid login data.
        3. Make a POST request to simulate a failed login.
        4. Check the response status code and content.
        5. Assert that the response indicates failure.
        """
        # Create invalid login data with incorrect password
        login_data = {
            'username': 'john@example.com',  # Using email as the username
            'password': 'incorrectpassword',
        }

        # Use app.test_request_context() to create an application context
        with app.test_request_context(
            '/api/v1/sign_in',
            method='POST',
            data=json.dumps(login_data),
            content_type='application/json',
        ):
            response = signin_resource.post()

            response_data = response[0]
            response_status = response[1]

            assert response_status == 401

            assert 'message' in response_data
            assert 'status' in response_data
            assert response_data['status'] == 'failed'
            assert response_data['message'] == 'Authentication failed.'
