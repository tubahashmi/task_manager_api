from unittest.mock import patch

import pytest

from apiserver.api.resources import SignupResource



@pytest.fixture
def signup_resource():
    """Create an instance of SignupResource"""
    return SignupResource()


class MockRole:
    def __init__(self, id=1):
        self.id = id

class MockUser:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

@pytest.fixture
def signup_resource_mock(app):
    # Mock the necessary methods and attributes of SignupResource
    with app.test_request_context():
        signup_resource = SignupResource()

        # Mock the Role.query.filter_by method to return a role with id 1
        user_query_mock = patch('apiserver.api.models.User.query')
        user_query_filter_by_mock = user_query_mock.start()

        # Modify the behavior to return None when the email already exists
        user_query_filter_by_mock.return_value.first.return_value = None

        # Mock the Role.query.filter_by method to return a role with id 1
        role_query_mock = patch('apiserver.api.models.Role.query')
        role_query_filter_by_mock = role_query_mock.start()
        role_query_filter_by_mock.filter_by.return_value = MockRole(id=1)
        # Modify the behavior to return None when the email already exists
        role_query_filter_by_mock.return_value.first.return_value = None

        yield signup_resource_mock

    # Clean up the mocks
    user_query_mock.stop()
    role_query_mock.stop()
    # Clean up other mocks as needed

@pytest.fixture
def user_already_exists(app):
    """Patch User.query.filter_by to return an existing user"""
    with app.test_request_context():
        user_query_mock = patch('apiserver.api.models.User.query')
        user_query_filter_by_mock = user_query_mock.start()

        # Modify the behavior to return an existing user when the email already exists
        user_query_filter_by_mock.return_value.first.return_value = MockUser(**{
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'hashed_password',  # Replace with the actual hashed password
        })

        yield user_query_mock

    # Clean up the mock
    user_query_mock.stop()







