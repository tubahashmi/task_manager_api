#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Module containing unit tests for the SigninResource class.
"""
#   pylint: disable=W0613,C0103,C0301

# Standard library
import json


class TestSignupResource:
    """
    Test cases for the SignupResource class.
    """

    def test_user_registration_with_valid_data_and_default_role(
        self, app, db, signup_resource
    ):  #   pylint: disable=W0613
        """
        Test user registration with valid data and default role.

        Args:
            app (Flask app): The Flask application context.
            db (Mock): Mocked database object.
            signup_resource (SignupResource): Instance of SignupResource for testing.

        Test steps:
        1. Create valid data with default role.
        2. Create a test request context with valid registration data.
        3. Make a POST request to simulate user registration.
        4. Check the response status code and content.
        5. Assert that the response indicates success and includes user details.
        """
        # Create valid data with default role
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'secretpassword',
        }

        with app.test_request_context(
            '/api/v1/sign_up',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
        ):
            response = signup_resource.post()

            response_data = response[0]
            response_status = response[1]

            assert response_status.value == 201
            assert response_data['status'] == 'success'
            assert 'id' in response_data['result']
            assert 'email' in response_data['result']
            assert 'firstName' in response_data['result']
            assert 'lastName' in response_data['result']
            assert 'createdAt' in response_data['result']
            assert 'role' in response_data['result']

    def test_user_registration_with_existing_email(
        self, app, user_already_exists, signup_resource
    ):
        """
        Test user registration with an existing email.

        Args:
            app (Flask app): The Flask application context.
            user_already_exists (MagicMock): Mocked User.query.filter_by for an existing user.
            signup_resource (SignupResource): Instance of SignupResource for testing.

        Test steps:
        1. Create data with an existing email address.
        2. Create a test request context with the existing email data.
        3. Make a POST request to simulate user registration.
        4. Check the response status code and content.
        5. Assert that the response indicates failure due to an existing user.
        """
        # Create data with an existing email address
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',  # Existing email address
            'password': 'secretpassword',
        }

        # Use app.test_request_context() to create an application context
        with app.test_request_context(
            '/api/v1/sign_up',
            method='POST',
            data=json.dumps(data),
            content_type='application/json',
        ):
            response = signup_resource.post()

            response_data = response[0]
            response_status = response[1]

            assert response_status.value == 409
            assert 'message' in response_data
            assert 'status' in response_data
            assert response_data['status'] == 'failed'
            assert response_data['message'] == 'User already exists.'
