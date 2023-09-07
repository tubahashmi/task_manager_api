import json

import pytest


class TestSignupResource:

    def test_user_registration_with_valid_data_and_default_role(self, app, db, signup_resource):
        # Create valid data with default role
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'secretpassword'
        }

        with app.test_request_context('/api/v1/sign_up', method='POST', data=json.dumps(data),
                                      content_type='application/json'):
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

    def test_user_registration_with_existing_email(self, app, user_already_exists, signup_resource):
        # Create data with an existing email address
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',  # Existing email address
            'password': 'secretpassword'
        }

        # Use app.test_request_context() to create an application context
        with app.test_request_context('/api/v1/sign_up', method='POST', data=json.dumps(data),
                                      content_type='application/json'):
            response = signup_resource.post()

            response_data = response[0]
            response_status = response[1]

            assert response_status.value == 409
            assert 'message' in response_data
            assert 'status' in response_data
            assert response_data['status'] == 'failed'
            assert response_data['message'] == 'User already exists.'