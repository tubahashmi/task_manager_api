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
ALLOWED_FIELDS_TO_UPDATE = [
    'title',
    'description',
    'due_date',
    'priority',
    'status',
    'estimate',
    'actual_time_spent'
]


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
    USER_ALREADY_EXISTS = 'User already exists.'
    FAILED_TO_DELETE_USER = 'Unable to delete user.'
    FAILED_TO_DELETE_COMMENT = 'Unable to delete comment.'
    FAILED_TO_ASSIGN_TASK = 'Unable to assign task to the user.'
    TASK_ASSIGNED = 'Task assigned successfully.'
    FAILED_TO_CREATE_TASK = 'Failed to create task.'
    TASK_CREATED = 'Task created successfully.'
    TASK_UPDATED = 'Task updated successfully.'
    COMMENT_DELETED = 'Comment successfully deleted.'

class PriorityLevel(enum.Enum):
    """Priority levels definition for a Task."""

    RELAXED = 'low'
    MEDIUM = 'medium'
    TIGHT = 'high'


class TaskStatus(enum.Enum):
    """Status types definition for a Task."""

    OPEN = 'open'
    IN_WORK = 'in work'
    COMPLETED = 'completed'
    DISCARD = 'discarded'


class TaskType(enum.Enum):
    """Task types definition for a Task."""

    TASK = 'task'
    SUBTASK = 'sub-task'
