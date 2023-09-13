# !./venv/bin/python
# -*- coding: utf-8 -*-

"""Defines User related APIs."""
# pylint: disable=C0301,W0718,W0612

# Standard library
from http import HTTPStatus

# Third-party
from flask import g, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

# First-party
from apiserver.api.models import Comment, Task, User
from apiserver.api.schemas.tasks import CommentSchema, TaskSchema
from apiserver.commons.constants import (
    ALLOWED_FIELDS_TO_UPDATE,
    APIResponse,
    APIResponseKeys,
    APIResponseMessage,
)
from apiserver.commons.helpers import (
    require_basic_auth,
    role_required,
    validate_fields,
    validate_input,
)
from apiserver.extensions import db


class TaskResource(Resource):
    """
    API Resource for task management.

    This resource allows users to create, retrieve, update, and delete tasks.

    Attributes:
        method_decorators (list): A list of method decorators to apply to the resource methods.
    """

    method_decorators = [
        require_basic_auth,
    ]

    @role_required('admin')
    @validate_input(
        {
            'title': ['required'],
        }
    )
    def post(self):
        """
        Create a new task.

        This endpoint allows an admin user to create a new task.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Task Management
        security:
          - basicAuth: []
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  title:
                    type: string
                    example: "Task Title"
                  description:
                    type: string
                    example: "Task description goes here"
                  due_date:
                    type: string
                    format: date
                    example: "2023-09-15"
                  priority:
                    type: string
                    example: "HIGH"
                  status:
                    type: string
                    example: "OPEN"
                  assigned_to_id:
                    type: integer
                    example: 1
                  recurring_task:
                    type: boolean
                    example: true
                  estimate:
                    type: integer
                    example: 5
                  actual_time_spent:
                    type: integer
                    example: 3
        definitions:
          TaskSchema:
            type: object
            properties:
              id:
                type: integer
                example: 1
              title:
                type: string
                example: "Complete Project Report"
              description:
                type: string
                example: "Write a comprehensive project report by Friday."
              assigned_to_id:
                type: integer
                example: 1
              created_by_id:
                type: integer
                example: 1
              created_at:
                type: string
                format: date-time
                example: "2023-09-05T12:00:00Z"
              updated_at:
                type: string
                format: date-time
                example: "2023-09-06T14:30:00Z"
        responses:
          201:
            description: Task created successfully
            content: application/json
            schema:
              $ref: "#/definitions/TaskSchema"
          400:
            description: Task creation failed
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Failed to create task"
                status:
                  type: string
                  example: "error"
        """
        try:
            data = request.get_json()
        except Exception as _e:
            return {
                'message': APIResponseMessage.FAILED_TO_CREATE_TASK.value,
                'status': APIResponse.FAIL.value,
            }, HTTPStatus.BAD_REQUEST
        task = Task.query.filter_by(title=data.get('title')).first()
        if task:
            return {
                'message': f'Task \'{task.title}\' <{task.id}>  already exists',
                'status': APIResponse.FAIL.value,
            }, HTTPStatus.CONFLICT

        new_task = Task(**data)
        new_task.created_by_id = g.current_user.id
        db.session.add(new_task)
        db.session.commit()
        try:
            db.session.commit()
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_CREATED.value,
                APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
                APIResponseKeys.RESULT.value: TaskSchema().dump(new_task),
            }, HTTPStatus.CREATED
        except Exception as _e:
            return {
                'message': APIResponseMessage.FAILED_TO_CREATE_TASK.value,
                'status': APIResponse.FAIL.value,
            }, HTTPStatus.BAD_REQUEST

    def get(self):
        """
        Retrieve a list of tasks or a specific task.

        This endpoint allows an admin user to retrieve a list of all tasks or a specific task by providing the task ID.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Task Management
        security:
          - basicAuth: []
        parameters:
          - in: query
            name: task_id
            required: false
            type: string
            description: The ID of the task to retrieve (optional).
        definitions:
          TaskSchema:
            type: object
            properties:
              id:
                type: string
                example: "123abc"
              title:
                type: string
                example: "Complete Project Report"
              description:
                type: string
                example: "Write a comprehensive project report by Friday."
              assigned_to_id:
                type: integer
                example: 1
              created_by_id:
                type: integer
                example: 1
              created_at:
                type: string
                format: date-time
                example: "2023-09-05T12:00:00Z"
              updated_at:
                type: string
                format: date-time
                example: "2023-09-06T14:30:00Z"

        responses:
          200:
            description: Task list or task retrieved successfully
            content: application/json
            schema:
              type: object
              properties:
                results:
                  type: array
                  items:
                    $ref: "#/definitions/TaskSchema"
                status:
                  type: string
                  example: "success"
          404:
            description: Task not found
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Task does not exist"
                status:
                  type: string
                  example: "error"
        """
        task_id = request.args.get('task_id')
        if task_id:
            task = Task.query.filter_by(id=task_id).first()
            if task:
                return {
                    APIResponseKeys.RESULT.value: TaskSchema().dump(task),
                    APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
                }, HTTPStatus.OK
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_NOT_FOUND.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.NOT_FOUND

        tasks = Task.query.order_by('created_at').all()

        return {
            APIResponseKeys.RESULT.value: TaskSchema(many=True).dump(tasks),
            APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
        }, HTTPStatus.OK

    @validate_fields(ALLOWED_FIELDS_TO_UPDATE)
    def put(self, task_id):
        """
        Update a task.

        This endpoint allows an admin user to update a specific task by providing the task ID and the updated data.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Task Management
        security:
          - basicAuth: []
        parameters:
          - in: path
            name: task_id
            required: true
            type: string
            description: The ID of the task to update.
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  title:
                    type: string
                    example: "Updated Task Title"
                  description:
                    type: string
                    example: "Updated task description goes here"
                  due_date:
                    type: string
                    format: date
                    example: "2023-09-20"
                  priority:
                    type: string
                    example: "LOW"
                  status:
                    type: string
                    example: "IN_PROGRESS"
                  assigned_to_id:
                    type: intger
                    example: 1
                  recurring_task:
                    type: boolean
                    example: false
                  estimate:
                    type: integer
                    example: 10
                  actual_time_spent:
                    type: integer
                    example: 7
        responses:
          201:
            description: Task updated successfully
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Task updated successfully"
                status:
                  type: string
                  example: "success"
          404:
            description: Task not found
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Task not found"
                status:
                  type: string
                  example: "error"
        """
        task = Task.query.get(task_id)
        if not task:
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_NOT_FOUND.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.NOT_FOUND

        # Update task attributes based on request data
        data = request.get_json()
        for key, value in data.items():
            setattr(task, key, value)
        db.session.commit()
        return {
            APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_UPDATED.value,
            APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
        }, HTTPStatus.CREATED

    @role_required('admin')
    def delete(self, task_id):
        """
        Delete a task.

        This endpoint allows an admin user to delete a specific task by providing the task ID.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Task Management
        security:
          - basicAuth: []
        parameters:
          - in: path
            name: task_id
            required: true
            type: string
            description: The ID of the task to delete.
        responses:
          200:
            description: Task deleted successfully
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Task deleted successfully"
                status:
                  type: string
                  example: "success"
          404:
            description: Task not found
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Task not found"
                status:
                  type: string
                  example: "error"
        """
        task = Task.query.get(task_id)
        if not task:
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_NOT_FOUND.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.NOT_FOUND

        db.session.delete(task)
        db.session.commit()
        return {
            APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_DELETED.value,
            APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
        }, HTTPStatus.OK


class CommentResource(Resource):
    """
    API Resource for managing comments on tasks.

    This resource allows users to create, retrieve, update, and delete comments on tasks.

    Attributes:
        method_decorators (list): A list of method decorators to apply to the resource methods.
    """

    method_decorators = [require_basic_auth]

    @validate_input({'comment': ['required']})
    def post(self, task_id):
        """
        Create a new comment on a task.

        This endpoint allows an authenticated user to add a new comment to a task.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Comment Management
        security:
          - basicAuth: []
        parameters:
          - in: path
            name: task_id
            required: true
            type: string
            description: The ID of the task to which the comment will be added.
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  comment:
                    type: string
                    example: "This is a comment on the task."
        definitions:
          CommentSchema:
            type: object
            properties:
              id:
                type: string
                example: "123abc"
              content:
                type: string
                example: "This is a comment on the task."
              task_id:
                type: string
                example: "456def"
              created_by_id:
                type: string
                example: "789ghi"
              created_at:
                type: string
                format: date-time
                example: "2023-09-05T15:45:00Z"
              updated_at:
                type: string
                format: date-time
                example: "2023-09-06T09:20:00Z"
        responses:
          201:
            description: Comment created successfully
            content: application/json
            schema:
              $ref: "#/definitions/CommentSchema"
          400:
            description: Comment creation failed
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Failed to create comment"
                status:
                  type: string
                  example: "error"
        """

        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_NOT_FOUND.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.NOT_FOUND

        data = request.get_json()
        new_comment = Comment(content=data.get('comment'))
        task.comments.append(new_comment)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.FAILED_TO_DELETE_COMMENT.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.BAD_REQUEST

        return {
            APIResponseKeys.RESULT.value: CommentSchema().dump(new_comment),
            APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
        }, HTTPStatus.CREATED

    def get(self, task_id):
        """
        Retrieve all comments on a task.

        This endpoint allows an authenticated user to retrieve all comments on a specific task.

        Returns:
            list: A list containing comment data.
        ---
        tags:
          - Comment Management
        security:
          - basicAuth: []
        parameters:
          - in: path
            name: task_id
            required: true
            type: string
            description: The ID of the task to retrieve comments from.
        definitions:
          CommentSchema:
            type: object
            properties:
              id:
                type: string
                example: "123abc"
              content:
                type: string
                example: "This is a comment on the task."
              task_id:
                type: string
                example: "456def"
              created_by_id:
                type: string
                example: "789ghi"
              created_at:
                type: string
                format: date-time
                example: "2023-09-05T15:45:00Z"
              updated_at:
                type: string
                format: date-time
                example: "2023-09-06T09:20:00Z"
        responses:
          200:
            description: Comments retrieved successfully
            content: application/json
            schema:
              type: array
              items:
                $ref: "#/definitions/CommentSchema"
          404:
            description: Task not found
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Task not found"
                status:
                  type: string
                  example: "error"
        """
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_NOT_FOUND.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.NOT_FOUND
        comments = [comment.to_json() for comment in task.comments]
        return {
            APIResponseKeys.RESULT.value: comments,
            APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
        }, HTTPStatus.OK

    @validate_input({'comment': ['required']})
    def put(self, task_id, comment_id):
        """
        Update a comment on a task.

        This endpoint allows an authenticated user to update a comment on a specific task.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Comment Management
        security:
          - basicAuth: []
        parameters:
          - in: path
            name: task_id
            required: true
            type: string
            description: The ID of the task containing the comment.
          - in: path
            name: comment_id
            required: true
            type: string
            description: The ID of the comment to update.
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  comment:
                    type: string
                    example: "Updated comment content."
        definitions:
          CommentSchema:
            type: object
            properties:
              id:
                type: string
                example: "123abc"
              content:
                type: string
                example: "This is a comment on the task."
              task_id:
                type: string
                example: "456def"
              created_by_id:
                type: string
                example: "789ghi"
              created_at:
                type: string
                format: date-time
                example: "2023-09-05T15:45:00Z"
              updated_at:
                type: string
                format: date-time
                example: "2023-09-06T09:20:00Z"
        responses:
          200:
            description: Comment updated successfully
            content: application/json
            schema:
              $ref: "#/definitions/CommentSchema"
          404:
            description: Comment or task not found
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Comment or task not found"
                status:
                  type: string
                  example: "error"
        """
        task = Task.query.filter_by(id=task_id).first()
        if not task:
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_NOT_FOUND.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.NOT_FOUND
        comment = Comment.query.filter_by(id=comment_id).first()
        if not comment:
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.COMMENT_NOT_FOUND.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.NOT_FOUND

        data = request.get_json()
        comment.content = data.get('comment', comment.content)

        db.session.commit()

        return {
            APIResponseKeys.RESULT.value: comment.to_json(),
            APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
        }, HTTPStatus.OK

    def delete(self, task_id, comment_id):
        """
        Delete a comment on a task.

        This endpoint allows an authenticated user to delete a comment from a specific task.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Comment Management
        security:
          - basicAuth: []
        parameters:
          - in: path
            name: task_id
            required: true
            type: string
            description: The ID of the task containing the comment.
          - in: path
            name: comment_id
            required: true
            type: string
            description: The ID of the comment to delete.
        responses:
          200:
            description: Comment deleted successfully
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Comment deleted successfully"
                status:
                  type: string
                  example: "success"
          404:
            description: Comment or task not found
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Comment or task not found"
                status:
                  type: string
                  example: "error"
        """
        task = Task.query.filter_by(id=task_id).first()
        comment = Comment.query.filter_by(id=comment_id).first()

        if not (comment and task):
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.RESOURCE_NOT_FOUND.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.NOT_FOUND

        db.session.delete(comment)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.FAILED_TO_DELETE_COMMENT.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.BAD_REQUEST

        return {
            APIResponseKeys.MESSAGE.value: APIResponseMessage.COMMENT_DELETED.value,
            APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
        }, HTTPStatus.OK


class AssignTaskResource(Resource):
    """
    API Resource for assigning tasks to users.

    This resource allows admins to assign tasks to users.

    Attributes:
        method_decorators (list): A list of method decorators to apply to the resource methods.
    """

    method_decorators = [
        role_required('admin'),  # Only admins can assign tasks to users
        require_basic_auth,
    ]

    @validate_input({'user_id': ['required'], 'task_id': ['required']})
    def post(self):
        """
        Assign a task to a user.

        This endpoint allows an admin to assign a task to a user.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Task Assignment
        security:
          - basicAuth: []
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  example: 1
                task_id:
                  type: integer
                  example: 1
        definitions:
          TaskSchema:
            type: object
            properties:
              id:
                type: integer
                example: 1
              title:
                type: string
                example: "Complete Project Report"
              description:
                type: string
                example: "Write a comprehensive project report by Friday."
              assigned_to_id:
                type: integer
                example: 1
              created_by_id:
                type: integer
                example: 1
              created_at:
                type: string
                format: date-time
                example: "2023-09-05T12:00:00Z"
              updated_at:
                type: string
                format: date-time
                example: "2023-09-06T14:30:00Z"
        responses:
          201:
            description: Task assigned successfully
            content: application/json
            schema:
              $ref: "#/definitions/TaskSchema"
          400:
            description: Task assigned successfully
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Failed to assign task"
                status:
                  type: string
                  example: "error"
        """
        data = request.get_json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')

        user = User.query.filter_by(id=user_id).first()
        task = Task.query.filter_by(id=task_id).first()
        if not (user and task):
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.RESOURCE_NOT_FOUND.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.NOT_FOUND

        # Assign the task to the user
        task.assigned_to_id = user_id

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {
                APIResponseKeys.MESSAGE.value: APIResponseMessage.FAILED_TO_ASSIGN_TASK.value,
                APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
            }, HTTPStatus.BAD_REQUEST

        return {
            APIResponseKeys.MESSAGE.value: APIResponseMessage.TASK_ASSIGNED.value,
            APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
            APIResponseKeys.RESULT.value: TaskSchema().dump(task),
        }, HTTPStatus.CREATED


class AssignedTasksListResource(Resource):
    """
    API Resource for retrieving tasks assigned to the current user.

    This resource allows authenticated users to retrieve tasks assigned to them.

    Attributes:
        method_decorators (list): A list of method decorators to apply to the resource methods.
    """

    method_decorators = [
        jwt_required(),
    ]

    def get(self):
        """
        Retrieve tasks assigned to the current user.

        This endpoint allows an authenticated user to retrieve tasks assigned to them.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Task Assignment
        security:
          - authBearer: []
        definitions:
          TaskSchema:
            type: object
            properties:
              id:
                type: integer
                example: 1
              title:
                type: string
                example: "Complete Project Report"
              description:
                type: string
                example: "Write a comprehensive project report by Friday."
              assigned_to_id:
                type: integer
                example: 1
              created_by_id:
                type: integer
                example: 1
              created_at:
                type: string
                format: date-time
                example: "2023-09-05T12:00:00Z"
              updated_at:
                type: string
                format: date-time
                example: "2023-09-06T14:30:00Z"

        responses:
          200:
            description: Assigned tasks retrieved successfully
            content: application/json
            schema:
              type: array
              items:
                $ref: "#/definitions/TaskSchema"
          404:
            description: No assigned tasks found
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "No assigned tasks found"
                status:
                  type: string
                  example: "error"
        """
        current_user_id = get_jwt_identity()
        tasks = Task.query.filter_by(assigned_to_id=current_user_id).all()

        return {
            APIResponseKeys.RESULT.value: TaskSchema(many=True).dump(tasks),
            APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
        }, HTTPStatus.OK
