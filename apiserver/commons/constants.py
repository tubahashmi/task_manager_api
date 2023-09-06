#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Contain constants for this application."""

# Standard library
import enum

import uuid
from datetime import datetime

# Define constants for string literals
TASK_UUID_DEFAULT = str(uuid.uuid4())
TASK_DATETIME_DEFAULT = datetime.utcnow()
TASKS_ID = 'tasks.id'

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

    FAILED_TO_FETCH_USERS_LIST = 'Unable to fetch users.'
    FAILED_TO_FETCH_USER = 'Failed to fetch User.'
    DELETED_USER = 'User deleted successfully.'
    FAILED_TO_SIGN_UP = 'Failed to Sign Up.'
    USER_NOT_FOUND = 'User not found.'
    AUTHENTICATION_FAILED = 'Authentication failed.'
    ACCESS_DENIED = 'Access denied. You don\'t have the required role.'
    INVALID_CREDENTIALS = 'Invalid credentials.'
    MISSING_AUTH_HEADER = 'Authorization header not found.'
    USER_DELETED = 'User deleted successfully.'
    USER_ALREADY_EXISTS = 'User already exists.'
    FAILED_TO_DELETE_USER = 'Unable to delete user.'


class PriorityLevel(enum.IntEnum):
    """Priority levels definition for a Task."""

    RELAXED = 0 # low
    MEDIUM = 1  # medium
    TIGHT = 2   # high


class TaskStatus(enum.IntEnum):
    """Status types definition for a Task."""

    OPEN = 0
    IN_WORK = 1
    COMPLETED = 2
    DISCARD = 3
