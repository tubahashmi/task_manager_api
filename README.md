# Task Management API [A Software Engineering Task]

## Overview

[Task description](https://drive.google.com/file/d/1frcBcIyzwzNyXy0yThwCkgYD2tlY_DMV/view?usp=sharing)

## Architecture

Task Management API backend application consists the following components:

- [Flask](https://flask.palletsprojects.com/en/latest/)
- [MySQL](https://www.mysql.org/)

### Flask

- Flask serves as the API server for TaskManagement application and is implemented using [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/) extension.
- Data served by this backend application is persisted using MySQL.

### MySQL

- MySQL database is used to persist data served by Flask backend.

## Setup


### Repository

Clone **[task_manager_api](https://github.com/tubahashmi/task_manager_api.git)** repository.

```sh
git clone git@github.com:tubahashmi/task_manager_api.git
cd task_management_api
```

### Virtual Environment

Create a new Python virtual environment.

```sh
pip install virtualenv
```

```
python3 -m venv venv
```

Install the latest requirements in the `virtualenv` after activating it.

```sh
source venv/bin/activate
```
```
pip install -r requirements.txt
```

### Variables

Export the following environment variables, once the requirements have been installed.

***NOTE:** All these variables should be defined in [.env]()

```shell script
export PYTHONPATH=/path/to/project/
export ROOT_PATH=/path/to/project
export UNIT_TESTING=True
export PYTHONUNBUFFERED=1
export FLASK_ENV=development
export FLASK_APP=app:create_app
export DATABASE_URI=mysql://admin:admin@localhost/taskmanagerdb
export MYSQL_USER=admin
export MYSQL_PASSWORD=admin
export MYSQL_HOST=localhost
export MYSQL_PORT=5432
export MYSQL_DB=taskmanagerdb
export FLASK_DEBUG=1
export LOG_FILE_PATH=/var/log/taskmanager
export JWT_SECRET_KEY=changemeplease
```

### Project Tree

```shell script
.
├── apiserver
│   ├── api
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   ├── roles.py
│   │   │   ├── tasks.py
│   │   │   └── users.py
│   │   ├── resources
│   │   │   ├── __init__.py
│   │   │   ├── tasks.py
│   │   │   └── users.py
│   │   ├── schemas
│   │   │   ├── __init__.py
│   │   │   ├── roles.py
│   │   │   ├── tasks.py
│   │   │   └── users.py
│   │   ├── __init__.py
│   │   └── views.py
│   ├── commons
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── helpers.py
│   │   ├── logging.ini
│   │   ├── logging.py
│   │   └── utilities.py
│   ├── migrations
│   │   ├── versions
│   │   │   ├── 2e9e81efe544_.py
│   │   │   ├── 86b4af4e598e_.py
│   │   │   ├── __init__.py
│   │   │   └── bfcafce07ea9_.py
│   │   ├── README
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── data_management.py
│   ├── extensions.py
│   ├── manage.py
│   └── run.py
├── deployment
│   ├── local
│   │   ├── Dockerfile
│   │   └── start
│   ├── production
│   ├── staging
│   └── __init__.py
├── postman
│   └── postman_collection.json
├── template
│   ├── data
│   │   ├── comments.json
│   │   ├── roles.json
│   │   ├── tasks.json
│   │   └── users.json
│   └── __init__.py
├── tests
│   ├── test_comments
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_add_comment.py
│   │   ├── test_delete_comment.py
│   │   ├── test_fetch_comments.py
│   │   └── test_update_comment.py
│   ├── test_signin
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── test_signin.py
│   ├── test_signup
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── test_signup.py
│   ├── README.md
│   ├── __init__.py
│   ├── config.py
│   └── conftest.py
├── CHANGELOG.md
├── Makefile
├── README.md
├── TODO.md
├── cspell.json
├── docker-compose.yaml
└── requirements.txt
```

### MySQL Configuration

#### Installation

Install MySQL and start the services.

##### MacOS

***NOTE:** For reference follow this link: .*

```sh
brew install mysql
pg_ctl -D /usr/local/var/mysql start && brew services start mysql
mysql -V
```

#### Configuration

Login into the MySQL terminal.

```sh
mysql -u root
```

Create user `admin` if not already present and grant privileges to the user.

```sql
CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
```

Exit the terminal and login again with `admin` user.

```sql
\q
mysql -u admin
```

Create `taskmanagerdb` database and connect to it.

```sql
CREATE DATABASE taskmanagerdb;
USE taskmanagerdb;
```

Exit MySQL shell.

```sql
\q
```

### Logging

Once the database has been setup, we will create the logs directory `/var/log/taskmanager` and change permission of the directory.

```sh
sudo mkdir /var/log/taskmanager
sudo chmod 777 /var/log/taskmanager/
```

After this we will start the Flask app along with New Relic APM.

### Start Flask App

Go to project root directory.

```sh
cd ./task_manager_api/
```

Now go to `./apiserver` directory from the root directory.

```sh
cd ./apiserver/
```

Start the app by running the following command.

```sh
flask run -h 0.0.0.0
```

## API Documentation and Swagger Support

Swagger has been set up to generate the API documentation automatically for each operation which is a combination of path and method, for each parameter, and for each response element.

When the flask server is up, this documentation can be viewed at:

```shell
http://localhost:5000/apidocs/#/
```

### Migration and Data Population

After starting Flask, we will apply migration and populate the data in database.

For applying migrations (present at `task_manager_api/apiserver/migrations`), open a new terminal and execute the following Flask command.


```sh
flask db upgrade
```

You should see a similar output.

```txt
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> bfcafce07ea9, empty message
```

Create database with all the tables.

***NOTE:** This step is only required once during initial setup.*

```sh
flask init
```

Once the migrations have been applied to the database, the data can be populated.


## Data Management and Maintenance

In order to insert data in the database and to manage it, a Python script `./apiserver/data_management.py` can be used as follows:

***NOTE:** This script should be run in any way to define roles in the system.*

```shell
python data_management.py
```

### Description

```txt
Script for populating and maintaining database using template files.

usage: data_management.py [-h] -c {users, tasks, comments, all} [{users, tasks, comments, all} ...]

Examples:
python data_management.py
python data_management.py -c all
python data_management.py -c users
python data_management.py -c tasks
python data_management.py -c tasks comments

```
Purpose is to pre-populate with dummy data in files.


## Unit Tests

Following unit tests are added:

**Sign Up**
- Positive Case: Sign Up with valid data (POST)
- Negative Case: Sign Up with invalid data (POST)

**Log In**
- Positive Case: Login with valid creds (POST)
- Negative Case: Login with invalid cred (POST)

**Add Comment**
- Positive Case: Add a valid comment (POST)
- Negative Case: Add an invalid comment (POST)

**Update Comment**
- Positive Case: Update a comment with valid task_id and comment_id data (PUT)
- Negative Case: Update a comment with invalid task_id (PUT)
- Negative Case: Update a comment with invalid comment_id (PUT)

**Fetch Comment**
- Positive Case: Fetch comments on valid task_id (GET)
- Negative Case: Fetch comments on invalid task_id (GET)

**Delete Comment**
- Positive Case: Delete a comment with valid task_id and comment_id (DELETE)
- Negative Case: Delete a comment with invalid task_id (DELETE)
- Negative Case: Delete a comment with invalid comment_id (DELETE)

Further details on unitests can be found in [README.md](https://github.com/tubahashmi/task_manager_api/blob/main/tests/README.md) of `tests/`

**Current coverage is **82%** and report can be found at [index.html](https://github.com/tubahashmi/task_manager_api/blob/main/tests/index.html)**


## Setup for Testing API Server

Using **[Postman](https://www.postman.com/)**, API(s) can be tested with ease.

### HTTP Requests

#### User Registration
##### Sign Up:

```html
POST {{local-host}}/api/v1/sign_up HTTP/1.1
Content-Type: application/json

{
    "first_name" : "Another",
    "last_name" : "Hashmi",
    "email": "tuba@gmail.com",
    "password": "hello123",
    "role": "admin"
}
```
#### User Login
##### Sign In:

```html
POST {{local-host}}/api/v1/sign_in HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
Content-Type: application/json
```
##### Get User Info:

```html
GET {{local-host}}/api/v1/user_info HTTP/1.1
Authorization: Bearer {{task-management-access-token}}
```

#### Admin Access
##### List Users:

```html
GET {{local-host}}/api/v1/users HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
```
##### Delete User:

```html
DELETE {{local-host}}/api/v1/delete_user/6 HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
```

#### Tasks
##### Add a New Task:
```html
POST {{local-host}}/api/v1/tasks/add HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
Content-Type: application/json

{
    "title": "Three New Task"
}
```

##### Fetch a Task by ID as Admin:

```html
GET {{local-host}}/api/v1/tasks?task_id=4 HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}

```
##### Fetch All Tasks as Admin:

```html
GET {{local-host}}/api/v1/tasks HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
```

##### Assign Task to a User:

```html
POST {{local-host}}/api/v1/assign-task HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
Content-Type: application/json

{
    "user_id": "3",
    "task_id": "4"
}

```

##### Update a Task:

```html
PUT {{local-host}}/api/v1/tasks/4 HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
Content-Type: application/json

{
    "description": "I'll not be deleted"
}

```
##### Delete a Task:
```html
DELETE {{local-host}}/api/v1/tasks/4 HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}

```
Retrieve All Tasks Assigned:
```html
GET {{local-host}}/api/v1/assigned-tasks-list HTTP/1.1
Authorization: Bearer {{task-management-access-token}}
```

#### Comments
##### Add Comment to a Task:
```html
POST {{local-host}}/api/v1/tasks/100/comments HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
Content-Type: application/json

{
    "comment": "coment 4"
}

```
##### Delete Comment from a Task:

```html
DELETE {{local-host}}/api/v1/tasks/1/comments/40 HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
```

##### Update a Comment on a Task:

```html
PUT {{local-host}}/api/v1/tasks/1/comments/43 HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
Content-Type: application/json

{
    "comment": "edited comment 4"
}
```

##### List all Comments on a Task:

```html
GET {{local-host}}/api/v1/tasks/1/comments HTTP/1.1
Authorization: Basic {{basic-auth-credentials}}
```

Replace {{local-host}}, {{basic-auth-credentials}}, and {{task-management-access-token}} with the appropriate values when making requests.




### Screenshots

Screenshots of the successful API calls can be found at [screenshots](https://github.com/tubahashmi/task_manager_api/tree/main/screenshots)