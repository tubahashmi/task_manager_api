# Task Management API - CHANGELOG

This file contains logs of all the changes made in this project.

## Authors

- Tuba Hashmi <hashmiatna@gmail.com>

## Maintainers

- Tuba Hashmi <hashmiatna@gmail.com>

---

## Before September 04, 2023

- NO CHANGELOG AVAILABLE

---

## September 05, 2023

- [x] Project structure set up.
- [x] Added the following files:
  - `requiremnets.txt`
  - `README.md`
  - `TODO.md`
  - `CHANGELOG.md`

---

## September 06, 2023

- [x] Merged branch `initialize-project-structure` ([PR#1](https://github.com/tubahashmi/task_manager_api/pull/1)).
- [x] Added the following files:
  - `apiserver/app.py` to create Flask App.
  - `apiserver/config.py` to add default configuration to Flask App.
  - `apiserver/extensions.py` for extension(s) registration.
  - `apiserver/manage.py` to support CLI management of Flask App.
  - `apiserver/run.py` to define entry point.
  - `apiserver/commons/constants.py` to define constants of the system.
  - `apiserver/commons/helpers.py` to define decorators.
  - `apiserver/commons/utilities.py` to define utility functions.
  - `apiserver/commons/logging.py` to define logger.
- [x] Merged branch `apiserver-setup` ([PR#2](https://github.com/tubahashmi/task_manager_api/pull/2)).
- [x] Added the following files to baseline apiserver:
  - `apiserver/api/__init__.py`
  - `apiserver/api/models/__init__.py`
  - `apiserver/api/resources/__init__.py`
  - `apiserver/api/schemas/__init__.py`
  - `apiserver/api/views.py`
- [x] Merged branch `apiserver-setup` ([PR#3](https://github.com/tubahashmi/task_manager_api/pull/3)).
- [x] Defined model 'Role' for table `roles` in the db. Added the following files:
  - `apiserver/api/models/roles.py`
  - `apiserver/api/schemas/roles.py`
- [x] Updated the following files:
  - `apiserver/api/models/__init__.py`
  - `apiserver/api/schemas/__init__.py`
- [x] Added migration for `roles`: `apiserver/migrations/versions/86b4af4e598e_.py`.
- [x] Added `apiserver/data_management.py` to populate roles: `admin` and `user` in table `roles`.
- [x] Merged branch `api-roles-resource` ([PR#4](https://github.com/tubahashmi/task_manager_api/pull/4)).
- [x] Defined model 'User' for table `users` in the db. Added the following files:
  - `apiserver/api/models/users.py`
  - `apiserver/api/schemas/users.py`
- [x] Added `apiserver/api/resources/users.py` to define HTTP methods.
- [x] Updated `apiserver/api/views.py` to expose API endpoints.
- [x] Added migration for table `users`: `migrations/versions/bfcafce07ea9_.py`.
- [x] Added logging configuration: `logging.ini`.
- [x] Merged branch `api-user-resource` ([PR#5](https://github.com/tubahashmi/task_manager_api/pull/5)).
- [x] Defined model 'User' for table `users` in the db. Added the following files:
  - `apiserver/api/models/users.py`
  - `apiserver/api/schemas/users.py`
- [x] Added `apiserver/api/resources/users.py` to define HTTP methods.
- [x] Updated `apiserver/api/views.py` to expose API endpoints.
- [x] Added migration for table `users`: `migrations/versions/bfcafce07ea9_.py`.
- [x] Added logging configuration: `logging.ini`.
- [x] Defined model 'Task' for table `tasks` in the db. 
- [x] Defined model 'SubTask' for table `subtasks` in the db.
- [x] Defined model 'Comment' for table `comments` in the db.
- [x] Defined model 'Dependency' for table `dependencies` in the db.
- [x] Added following files:
  - `apiserver/api/models/tasks.py`
- [x] Added migration for tables `tasks`, `subtasks`, `comments`, `dependencies` : `migrations/versions/f9647c5f0ee8_.py`.
- [x] Updated `CHANGELOG.md`.

---
