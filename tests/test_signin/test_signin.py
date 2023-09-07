import json
from unittest.mock import patch

from apiserver.api.models import User


def mock_authentication(username, password):
    # Return a user object with mocked credentials
    return User(email='john@example.com', password='hashed_password')


class TestSigninResource:

    def test_successful_user_login(self, app, signin_resource, user_authentication_success_mock):
        # Call the post method to simulate a successful login
        with app.test_request_context('/api/v1/sign_in', method='POST'):
            response = signin_resource.post()

            # Assert the response for success
            assert response[1] == 200
            assert 'access_token' in response[0]
            assert response[0]['status'] == 'success'

    def test_user_login_failure(self, app, signin_resource, user_authentication_failure_mock):
        # Create invalid login data with incorrect password
        login_data = {
            'username': 'john@example.com',  # Using email as the username
            'password': 'incorrectpassword'
        }

        # Use app.test_request_context() to create an application context
        with app.test_request_context('/api/v1/sign_in', method='POST', data=json.dumps(login_data),
                                      content_type='application/json'):
            response = signin_resource.post()

            response_data = response[0]
            response_status = response[1]

            assert response_status == 401

            assert 'message' in response_data
            assert 'status' in response_data
            assert response_data['status'] == 'failed'
            assert response_data['message'] == 'Authentication failed.'