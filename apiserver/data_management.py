#!./venv/bin/python
# -*- coding: utf-8 -*-

"""
Module for data population in the Task Manager application.

This module provides functionality to populate data into the database
for roles, users, tasks, and comments.

"""

# pylint: disable=C0301,W0718

# Standard library
import argparse
import json
import logging
import os
from random import choice
# Third-party
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# First-party
from apiserver.api.models import Comment, Task, User
from apiserver.api.models.roles import Role

logger = logging.getLogger('TaskManager.data_management')

DATABASE_URI = os.getenv('DATABASE_URI')

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the paths to your JSON files
roles_file = os.path.join(script_dir, '../template/data/roles.json')
users_file = os.path.join(script_dir, '../template/data/users.json')
tasks_file = os.path.join(script_dir, '../template/data/tasks.json')
comments_file = os.path.join(script_dir, '../template/data/comments.json')

# Create a SQLAlchemy engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()


def populate_roles():
    """Populate roles data from a JSON file."""
    with open(roles_file, 'r', encoding='utf-8') as file:
        roles_data = json.load(file)

    for role_data in roles_data['roles']:
        role_name = role_data.get('name')

        # Check if a role with the same name already exists
        existing_role = session.query(Role).filter_by(name=role_name).first()
        if existing_role:
            logger.info('Role <%s> already exists, skipping insertion', role_name)
        else:
            try:
                role = Role(**role_data)
                session.add(role)
                session.commit()
                logger.info('Role <%s> added to the user collection', role_name)
            except Exception:
                logger.info('Role <%s> failed to add to the user collection', role_name)


def populate_users():
    """Populate users data from a JSON file."""
    with open(users_file, 'r', encoding='utf-8') as file:
        users_data = json.load(file)
    for user_data in users_data['users']:
        try:
            user = User(**user_data)
            session.add(user)
            session.commit()
            logger.info('User <%s> added to the users collection', user_data.get('email'))
        except Exception:
            logger.error('User <%s> failed to add to the users collection', user_data.get('email'))


def populate_tasks():
    """Populate tasks data from a JSON file."""
    with open(tasks_file, 'r', encoding='utf-8') as file:
        tasks_data = json.load(file)

    users_ids = []
    # Load JSON data from tasks.json
    with open(users_file, 'r', encoding='utf-8') as file:
        users_data = json.load(file)

    for user_data in users_data['users']:
        email = user_data.get('email')

        # Query the users table to find the user record by email
        user = session.query(User).filter_by(email=email).first()
        users_ids.append(user.id)

    for task_data in tasks_data['tasks']:
        try:
            task = Task(**task_data)
            task.assigned_to_id = choice(users_ids)
            session.add(task)
            session.commit()
            logger.info('Task <%s> added to the tasks collection', task_data.get('title'))
        except Exception:
            logger.error('Task <%s> failed to add to the tasks collection', task_data.get('title'))


def populate_comments():
    """Populate comments data from a JSON file."""
    with open(comments_file, 'r', encoding='utf-8') as file:
        comments_data = json.load(file)
    tasks_ids = []
    # Load JSON data from tasks.json
    with open(tasks_file, 'r', encoding='utf-8') as file:
        tasks_data = json.load(file)

    for task_data in tasks_data['tasks']:
        title = task_data.get('title')

        # Query the tasks table to find the task record by title
        task = session.query(Task).filter_by(title=title).first()
        tasks_ids.append(task.id)

    for comment_data in comments_data['comments']:
        try:
            comment = Comment(**comment_data)
            comment.task_id = choice(tasks_ids)
            session.add(comment)
            session.commit()
            logger.info('Comment added to the comments collection')
        except Exception:
            logger.error('Comment <%s> failed to add to the comments collection', comment_data.get('content'))


def main():
    """Populate data tables based on command-line arguments.

    This function parses command-line arguments to determine which data tables to populate.

    Command-line options:
        -c, --collection: Specify the data collection to populate (choices: all, users, tasks, comments).

    Returns:
        None
    """
    try:
        logger.info('Data population begins.')

        # Parse command-line arguments
        parser = argparse.ArgumentParser(description='Populate data tables.')
        parser.add_argument('-c', '--collection', choices=['all', 'users', 'tasks', 'comments'],
                            help='Specify data collection')
        args = parser.parse_args()

        # Always populate roles
        populate_roles()

        # Check the collection argument and populate tables accordingly
        if args.collection == 'all':
            populate_users()
            populate_tasks()
            populate_comments()
        elif args.collection == 'users':
            populate_users()
        elif args.collection == 'tasks':
            populate_tasks()
        elif args.collection == 'comments':
            populate_comments()

        logger.info('Data population ends.')

    except Exception as e:  # pylint: disable=C0103
        session.rollback()
        logger.error('Error: {%s}', str(e))
    finally:
        session.close()


if __name__ == '__main__':
    main()
