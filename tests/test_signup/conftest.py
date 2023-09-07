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

@pytest.fixture
def db(app):
    """Patch db object inside flask app"""
    with app.test_request_context():
        db_mock = patch('apiserver.api.resources.users.db')
        db_mock_start = db_mock.start()

        yield db_mock_start

    # Clean up the mock
    db_mock.stop()