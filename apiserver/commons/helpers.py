#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Various helper functions and decorators"""
# Standard library
from functools import wraps
from http import HTTPStatus

# Third-party
from flask import g, request
from flask_jwt_extended import get_jwt_identity

# First-party
from apiserver.api.models import User
from apiserver.commons.constants import APIResponse, APIResponseKeys, APIResponseMessage
from apiserver.commons.utilities import authenticate_user, custom_unauthorized
from apiserver.extensions import basic_auth


def role_required(required_role):
    """
    Decorator to check if the current user has the required role.

    This decorator checks the role of the current user and ensures that they have
    the required role to access the decorated API endpoint.

    Args:
        required_role (str): The required role name.

    Returns:
        function: The wrapped function if the role is authorized, or a response
            indicating access denial.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'Authorization' in request.headers:
                # Check if the 'Authorization' header is present in the request
                authorization_header = request.headers['Authorization']
                if authorization_header.startswith('Bearer '):
                    # If the header starts with 'Bearer ', assume JWT authentication
                    current_user_id = get_jwt_identity()
                    current_user = User.query.get(current_user_id)
                else:
                    # If it doesn't start with 'Bearer ', assume Basic Authentication
                    username, password = (
                        request.authorization.username,
                        request.authorization.password,
                    )
                    current_user = authenticate_user(username, password)

                if not current_user:
                    return {
                        'message': APIResponseMessage.INVALID_CREDENTIALS.value
                    }, HTTPStatus.UNAUTHORIZED

                if current_user.role.name == required_role:
                    g.current_user = current_user
                    return func(*args, **kwargs)
                return {
                    'message': APIResponseMessage.ACCESS_DENIED.value
                }, HTTPStatus.FORBIDDEN
            return {
                'message': APIResponseMessage.MISSING_AUTH_HEADER.value
            }, HTTPStatus.UNAUTHORIZED

        return wrapper

    return decorator


@basic_auth.verify_password
def verify_password(email, password):
    """
    Verify user credentials for basic authentication.

    Args:
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    user = User.query.filter_by(email=email).first()
    if user:
        auth_user = authenticate_user(email, password)
        if auth_user:
            g.current_user = auth_user
            return True

    return False


def require_basic_auth(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return {
                'message': APIResponseMessage.MISSING_AUTH_HEADER.value
            }, HTTPStatus.UNAUTHORIZED
        username, password = (
            request.authorization.username,
            request.authorization.password,
        )
        current_user = authenticate_user(username, password)

        if not current_user:
            return {
                'message': APIResponseMessage.INVALID_CREDENTIALS.value
            }, HTTPStatus.UNAUTHORIZED

        g.current_user = current_user
        return func(*args, **kwargs)
    return decorator

def validate_input(validation_rules):
    """
    Middleware decorator to validate input data based on provided rules.

    Args:
        validation_rules (dict): A dictionary of field names and validation rules.

    Returns:
        function: Decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            errors = {}
            data = request.get_json()

            for field, rules in validation_rules.items():
                for rule in rules:
                    if rule == 'required' and field not in data:
                        errors[field] = f'{field} is required.'
            if errors:
                return {
                    'message': errors,  # Use plain string keys here
                    'status': APIResponse.ERROR.value,  # Or use plain string values here
                }, HTTPStatus.BAD_REQUEST
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_data(validation_function, key):
    """
    Middleware decorator to validate data using a custom validation function.

    Args:
        validation_function (function): The custom validation function.
        key (str): The key in the JSON data to validate.

    Returns:
        function: Decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            value = data.get(key)

            # Use the specified data validation function
            if validation_function(value):
                return func(*args, **kwargs)

            return {'errors': f'Invalid {key} format'}, HTTPStatus.BAD_REQUEST

        return wrapper

    return decorator


def validate_fields(allowed_fields):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()

            # Check if all fields in data are allowed
            disallowed_fields = [key for key in data.keys() if key not in allowed_fields]

            if disallowed_fields:
                error_message = {
                    str(APIResponseKeys.MESSAGE.value): f'Field(s) {", ".join(disallowed_fields)} not allowed to be updated.',
                    str(APIResponseKeys.STATUS.value): APIResponse.ERROR.value,
                }
                return error_message, HTTPStatus.BAD_REQUEST

            return func(*args, **kwargs)

        return wrapper

    return decorator
