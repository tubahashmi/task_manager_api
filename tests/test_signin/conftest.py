from http import HTTPStatus
from unittest.mock import patch
import pytest

from apiserver.api.resources import SigninResource



@pytest.fixture
def signin_resource():
    """Create an instance of SigninResource"""
    return SigninResource()

@pytest.fixture
def user_authentication_success_mock(app):
    """Mock a successful user authentication"""
    with app.test_request_context():
        mock = patch('apiserver.api.resources.SigninResource.post')
        mock_start = mock.start()

        # Simulate a successful authentication response
        response_data = {
            'access_token': 'your-access-token-here',
            'status': 'success',
        }
        # Set the side effect of the mock to return the success response
        mock_start.return_value = (response_data, HTTPStatus.OK)
        yield mock_start

    # Clean up the mock
    mock.stop()

@pytest.fixture
def user_authentication_failure_mock(app):
    """Mock a failed user authentication"""
    with app.test_request_context():
        mock = patch('apiserver.api.resources.SigninResource.post')
        mock_start = mock.start()

        # Simulate a failed authentication response
        response_data = {
            'message': 'Authentication failed.',
            'status': 'failed',
        }

        # Set the side effect of the mock to return the failure response
        mock_start.return_value = (response_data, HTTPStatus.UNAUTHORIZED)

        yield mock_start

    # Clean up the mock
    mock.stop()
