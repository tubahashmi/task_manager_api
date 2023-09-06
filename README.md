# Task Management API [A Software Engineering Task]

[TOC]

## Overview


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
virtualenv -p /usr/bin/python3 venv
```

Install the latest requirements in the `virtualenv` after activating it.

```sh
source venv/bin/activate
pip install -r requirements.txt
```

### Variables

Export the following environment variables, once the requirements have been installed.

***NOTE:** All these variables should be defined in **[.env]()** directory for different working environments (.development/.production/.staging).*

```shell script
export PYTHONPATH=/path/to/your/project
export UNIT_TESTING=True
export PYTHONUNBUFFERED=1
export BASIC_AUTH_USERNAME=admin
export BASIC_AUTH_PASSWORD=admin
export FLASK_ENV=development
export FLASK_APP=app:create_app
export DATABASE_URI=mysql://admin:admin@localhost:5432/yourdatabase
export MYSQL_USER=admin
export MYSQL_PASSWORD=admin
export MYSQL_HOST=localhost
export MYSQL_PORT=5432
export MYSQL_DB=yourdatabase
export ROOT_PATH=/path/to/your/project
```

### Project Tree

```shell script
.
├── apiserver
│   ├── models
│   │   └── __init__.py
│   ├── resources
│   │   └── __init__.py
│   ├── schemas
│   │   └── __init__.py
│   ├── __init__.py
│   ├── apiserver.py
│   ├── config.py
│   ├── extensions.py
│   ├── run.py
│   └── views.py
├── commons
│   ├── __init__.py
│   ├── constants.py
│   └── logging.py
├── tests
│   └── __init__.py
├── CHANGELOG.md
├── README.md
├── TODO.md
├── cspell.json
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
cd ./task_manager_api
```

### Migration and Data Population

After starting Flask, we will apply migration and populate the data in database.

For applying migrations (present at ``), open a new terminal and execute the following Flask command.


You should see a similar output.

```txt
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 5397d7b6a9c2, empty message
```

Create database with all the tables.

***NOTE:** This step is only required once during initial setup.*

```sh
flask init
```

Once the migrations have been applied to the database, the data can be populated.



## Data Management and Maintenance


## Setup for Testing API Server

Using **[Postman](https://www.postman.com/)**, API(s) can be tested with ease.

### HTTP Requests
