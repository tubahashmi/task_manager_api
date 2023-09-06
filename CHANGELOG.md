---
<!-- Project change log.

This file contains logs of all the changes made in this this project.

Usages:
  This file would normally document whatever changes made in this project
  like addition of a new feature, bug fix, general improvement, etc.

Authors:
  - Tuba Hashmi <tuba.hashmi@techwards.co>

Maintainers:
#   - Tuba Hashmi <tuba.hashmi@techwards.co>
-->
---

# Task Management API - CHANGELOG

---

## Before September 04, 2023

- NO CHANGELOG AVAILABLE

## September 05, 2023

- [x] Project structure set up.
- [x] Following files added:
    `requiremnets.txt`
    `README.md`
    `TODO.md`
    `CHANGELOG.md`
    
## September 06, 2023
- [x] Merged branch `initialize-project-structure` [PR#1](https://github.com/tubahashmi/task_manager_api/pull/1).
- [x] `apiserver/app.py` added to create Flask App.
- [x] `apiserver/config.py` added to add default configuration to Flask App.
- [x] `apiserver/extensions.py` added for extension(s) registration.
- [x] `apiserver/manage.py` added to support CLI management of Flask App
- [x] `apiserver/run.py` added to define entry point.
- [x] `apiserver/commons/constants.py` added to define constants of the system.
- [x] `apiserver/commons/helpers.py` added to define decorators.
- [x] `apiserver/commons/utilities.py` added to define utilities functions.
- [x] `apiserver/commons/logging.py` added to define logger.
- [x] Merged branch `apiserver-setup` [PR#2](https://github.com/tubahashmi/task_manager_api/pull/2).
- [x] Added following files to baseline apiserver:
    `apiserver/api/__init__.py`
    `apiserver/api/models/__init__.py`
    `apiserver/api/resources/__init__.py`
    `apiserver/api/schemas/__init__.py`
    `apiserver/api/views.py`
- [x] Merged branch `apiserver-setup` [PR#3](https://github.com/tubahashmi/task_manager_api/pull/3)
- [x] Defined 'Role' for table `role` in the db. Added following files:
    `apiserver/api/models/roles.py`
    `apiserver/api/schemas/roles.py`
- [x] Updated following files:
    `apiserver/api/models/__init__.py`
    `apiserver/api/schemas/__init__.py`
- [x] Added migration for `roles`: `apiserver/migrations/versions/86b4af4e598e_.py`.
- [x] Added `apiserver/data_management.py` to populate roles: `admin` and `user` in table `roles`.
- [x] `CHANGELOG.md` updated.

---
