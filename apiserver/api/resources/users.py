#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Defines User related APIs."""
from http import HTTPStatus

from flask import request, g
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource

from apiserver.api.models import User, Role
from apiserver.api.schemas import UserSchema
from apiserver.commons.constants import APIResponse, APIResponseKeys, APIResponseMessage
from apiserver.commons.helpers import role_required, validate_input, validate_data
from apiserver.commons.utilities import is_valid_email
from apiserver.extensions import db, basic_auth


class SignupResource(Resource):
    """
    API Resource for user registration (signup).

    This resource allows users to create an account by providing their information.

    Attributes:
        method_decorators (list): A list of method decorators to apply to the resource methods.
    """

    method_decorators = [
        validate_input({
            'first_name': ['required'],
            'last_name': ['required'],
            'email': ['required'],
            'password': ['required']
        }),
        validate_data(is_valid_email, 'email'),

    ]

    def post(self):
        """Registers a new user account with the system.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - User Registration
        requestBody:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  first_name:
                    type: string
                    example: "John"
                  last_name:
                    type: string
                    example: "Doe"
                  email:
                    type: string
                    format: email
                    example: "john@example.com"
                  password:
                    type: string
                    format: password
                    example: "secretpassword"
                  role:
                    type: string
                    example: "user"
        responses:
          201:
            description: User registration successful
            content: application/json
            schema:
                type: object
                properties:
                    status:
                        type: string
                        status: success
                    result:
                        allOf:
                        - $ref: '#/definitions/UserSchema'
          400:
            description: User registration failed
            content: application/json
            schema:
                  type: object
                  properties:
                    message:
                      type: string
                      example: "Unable to sign up"
                    status:
                      type: string
                      example: "error"
        """
        # Parse the request data
        data = request.get_json()
        if User.query.filter_by(email=data['email']).first():
            return {
                        APIResponseKeys.MESSAGE.value: APIResponseMessage.FAILED_TO_FETCH_USERS.value,
                        APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
                    },HTTPStatus.CONFLICT

        # Set the role to "user" if not provided
        role_id = Role.query.filter_by(name=data.get('role', 'user')).first().id

        # Create a new user with the role
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            role_id=role_id  # Use the role value from above
        )

        try:
            # Add the user to the database
            user.set_password(data['password'])
            db.session.add(user)
            db.session.commit()
        except:
            return {
                        APIResponseKeys.MESSAGE.value: APIResponseMessage.FAILED_TO_SIGN_UP.value,
                        APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
                    }, HTTPStatus.BAD_REQUEST

        # Return a response
        schema = UserSchema()
        result = schema.dump(user)
        return {
                    APIResponseKeys.RESULT.value: result,
                    APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
                }, HTTPStatus.CREATED


class SigninResource(Resource):
    """
    API Resource for user sign-in.

    This resource allows users to sign in and obtain an access token.

    Attributes:
        method_decorators (list): A list of method decorators to apply to the resource methods.
    """

    method_decorators = [
        basic_auth.login_required,
    ]

    def post(self):
        """Logs in the user using the provided username and password and generates an access token. The access token is required for subsequent API calls that require authentication via Bearer Token.
        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - User Sign In
        responses:
            200:
                description: 'User sign-in successful'
                content: application/json
                schema:
                    type: object
                    properties:
                        access_token:
                            type: string
                            example: "your-access-token-here"
                        status:
                            type: string
                            example: success
            401:
                description: 'User sign-in failed'
                content: application/json
                schema:
                    type: object
                    properties:
                        message:
                            type: string
                            example: "Authentication failed"
                        status:
                            type: string
                            example: "error"
        """
        try:
            current_user = g.current_user
            # Create an access token for the user
            access_token = create_access_token(identity=current_user.id)
            return {
                        APIResponseKeys.RESULT.value : {
                            'access_token': access_token,
                        },
                        APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
                    }, HTTPStatus.OK
        except Exception as _e:
            return {
                        APIResponseKeys.MESSAGE.value: APIResponseMessage.AUTHENTICATION_FAILED.value,
                        APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
                    }, HTTPStatus.BAD_REQUEST


class UserResource(Resource):
    """
    API Resource for user details.

    This resource allows authenticated users to retrieve their own user details.

    Attributes:
        method_decorators (list): A list of method decorators to apply to the resource methods.
    """

    method_decorators = [
        jwt_required(),
    ]

    def get(self):
        """
        Fetches logged in User's details.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - User Details
        security:
          - authBearer: []
        responses:
          200:
            description: User details retrieved successfully
            content: application/json
            schema:
                  $ref: "#/definitions/UserSchema"
          404:
            description: User not found
            content: application/json
            schema:
                  type: object
                  properties:
                    message:
                      type: string
                      example: "User not found"
                    status:
                      type: string
                      example: "fail"
        definitions:
          UserSchema:
            type: object
            properties:
              id:
                type: string
                example: 123abc
              first_name:
                type: string
                example: John
              last_name:
                type: string
                example: Doe
              email:
                type: string
                example: john.doe@example.com
        """
        current_user_id = get_jwt_identity()

        # Retrieve the user info of the authenticated user
        user = User.query.get(current_user_id)
        if user:
            schema = UserSchema()
            result = schema.dump(user)
            return {
                        APIResponseKeys.RESULT.value: result,
                        APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
                    }, HTTPStatus.OK
        else:
            return {
                        APIResponseKeys.MESSAGE.value: APIResponseMessage.USER_NOT_FOUND,
                        APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
                    }, HTTPStatus.NOT_FOUND


class UsersListResource(Resource):
    """List Users API.

    This resource allows users with the 'admin' role to retrieve a list of all users in the system.

    Attributes:
        method_decorators (list): A list of method decorators to apply to the resource methods.
    """
    method_decorators = [
        role_required('admin'),
        basic_auth.login_required(),
    ]

    def get(self):
        """Handle GET request for listing users.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - List all Users
        security:
          - basicAuth: []
        responses:
          200:
            description: List of users retrieved successfully
            content: application/json
            schema:
                type: object
                properties:
                        results:
                          type: array
                          items:
                            allOf:
                              - $ref: '#/definitions/UserSchema'
                        status:
                          type: string
                          example: "success"
          403:
            description: Access denied for non-admin users
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Access denied. You don't have the required role."
                status:
                  type: string
                  example: "error"
        definitions:
          UserSchema:
            type: object
            properties:
              id:
                type: integer
                example: 123abc
              first_name:
                type: string
                example: John
              last_name:
                type: string
                example: Doe
              email:
                type: string
                example: john.doe@example.com
        """
        # Retrieve list of all users in the system
        schema = UserSchema(many=True)
        try:
            query = User.query.order_by('created_at')
            return {
                       APIResponseKeys.RESULT.value: schema.dump(query),
                       APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value
                    }, HTTPStatus.OK
        except Exception as _e:
            return {
                        APIResponseKeys.MESSAGE.value: APIResponseMessage.FAILED_TO_FETCH_USERS_LIST.value,
                        APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
                    }, HTTPStatus.BAD_REQUEST


class DeleteAccount(Resource):
    """List Users API.

        This resource allows users with the 'admin' role to delete a users from the system.

        Attributes:
            method_decorators (list): A list of method decorators to apply to the resource methods.
    """
    method_decorators = [
        role_required('admin'),
        basic_auth.login_required(),
    ]
    def delete(self, user_id):
        """
        Deletes a user account with id <user_id>

        Args:
            user_id (int): The ID of the user to be deleted.

        Returns:
            tuple: A tuple containing response data and status code.
        ---
        tags:
          - Delete User
        security:
          - basicAuth: []
        parameters:
          - in: path
            name: user_id
            required: true
            type: integer
            description: The ID of the user to be deleted.
        responses:
          200:
            description: 'User deleted successfully'
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User deleted successfully."
                status:
                  type: string
                  example: "success"
          404:
            description: 'User not found'
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User does not exist."
                status:
                  type: string
                  example: "error"
          403:
            description: 'Access denied for non-admin users'
            content: application/json
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Access denied. You don't have the required role."
                status:
                  type: string
                  example: "error"
        """
        try:
            user = User.query.get(user_id)
            if user:
                # Delete the user from the database
                db.session.delete(user)
                db.session.commit()
                return {
                           APIResponseKeys.MESSAGE.value: 'User deleted successfully.',
                           APIResponseKeys.STATUS.value: APIResponse.SUCCESS.value,
                       }, HTTPStatus.OK
            else:
                return {
                           APIResponseKeys.MESSAGE.value: APIResponseMessage.USER_NOT_FOUND.value,
                           APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
                       }, HTTPStatus.NOT_FOUND
        except Exception as _e:
            return {
                       APIResponseKeys.MESSAGE.value: APIResponseMessage.FAILED_TO_DELETE_USER.value,
                       APIResponseKeys.STATUS.value: APIResponse.FAIL.value,
                   }, HTTPStatus.BAD_REQUEST
