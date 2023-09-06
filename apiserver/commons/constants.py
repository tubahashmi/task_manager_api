#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Contain constants for this application."""

# Standard library
import enum


class APIResponse(enum.Enum):
    """Enum for API response status."""

    FAIL = 'failed'  # APIResponse.FAIL.value
    SUCCESS = 'success'  # APIResponse.SUCCESS.value
    ERROR = 'error'  # APIResponse.ERROR.value


class APIResponseKeys(enum.Enum):
    """Enum for Messages in API Response JSON."""

    MESSAGE = 'message'
    STATUS = 'status'
    RESULT = 'result'


class APIResponseMessage(enum.Enum):
    """Enum for Status in API Response JSON."""

    FAILED_TO_FETCH_USER = 'Failed to fetch User.'
    FAILED_TO_SIGN_UP = 'Failed to Sign Up.'
    USER_NOT_FOUND = 'User not found.'
    AUTHENTICATION_FAILED = 'Authentication failed.'
    ACCESS_DENIED = 'Access denied. You don\'t have the required role.'
    INVALID_CREDENTIALS = 'Invalid credentials.'
    MISSING_AUTH_HEADER = 'Authorization header not found.'
    USER_DELETED = 'User deleted successfully.'
    USER_ALREADY_EXISTS= 'User already exists.'
