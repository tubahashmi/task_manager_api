# Standard library
import argparse
import json
import logging
import os
import sys
from random import choice

# Third-party
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# First-party
from apiserver.api.models import Comment, Task, User
from apiserver.api.models.roles import Role
from apiserver.commons.constants import PriorityLevel

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
    with open(roles_file, 'r') as file:
        roles_data = json.load(file)

    # Populate roles
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
            except Exception as _e:
                logger.info('Role <%s> failed to add to the user collection', role_name)

def populate_users():
    with open(users_file, 'r') as file:
        users_data = json.load(file)
    for user_data in users_data['users']:
        try:
            user = User(**user_data)
            session.add(user)
            session.commit()
            logger.info('User <%s> added to the users collection', user_data.get('email'))
        except Exception as _e:
            logger.error('User <%s> failed to add to the users collection', user_data.get('email'))
def populate_tasks():
    with open(tasks_file, 'r') as file:
        tasks_data = json.load(file)

    users_ids = []
    # Load JSON data from tasks.json
    with open(users_file, 'r') as file:
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
        except Exception as _e:
            logger.error('Task <%s> failed to add to the tasks collection', task_data.get('title'))

def populate_comments():
    with open(comments_file, 'r') as file:
        comments_data = json.load(file)
    tasks_ids = []
    # Load JSON data from tasks.json
    with open(tasks_file, 'r') as file:
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
        except Exception as _e:
            logger.error('Comment <%s> failed to add to the comments collection')

def main():
    try:
        logger.info('Data population begins.')

        # Parse command-line arguments
        parser = argparse.ArgumentParser(description='Populate data tables.')
        parser.add_argument('-c', '--collection', choices=['all', 'users', 'tasks', 'comments'], help='Specify data collection')
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

    except Exception as e:
        session.rollback()
        logger.error(f'Error: {e}')
    finally:
        session.close()

if __name__ == '__main__':
    main()