## Task Management API Backend Unit-testing
### Overview
The directory contains unit-tests for the backend application of Task Management App.
### Requirements

`coverage==6.5.0`

`pytest==7.2.0`

`WebTest==3.0.0`

- already added in requirements.txt
- if not installed already,
    
    `pip install coverage pytest webtest`

#### Run
1- Activate virtual environment

``source venv/bin/activate
``

2- Configure PYTHONPATH properly and set UNIT_TESTING to True

```export PYTHONPATH=__PATH_TO_ROOT_FOLDER__```

```export UNIT_TESTING=True```

3- Run tests

`coverage run -m pytest -v tests/ `

`coverage report -m`

**Output**
```shell
=========================================================================================== test session starts ============================================================================================
platform darwin -- Python 3.8.5, pytest-7.4.1, pluggy-1.3.0 -- /Users/tubahashmi/task_manager_api/venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/tubahashmi/task_manager_api
collected 14 items

tests/test_comments/test_add_comment.py::TestCommentResource::test_create_comment_with_valid_data PASSED                                                                                             [  7%]
tests/test_comments/test_add_comment.py::TestCommentResource::test_create_comment_with_invalid_task PASSED                                                                                           [ 14%]
tests/test_comments/test_delete_comment.py::TestCommentResource::test_delete_comment_with_valid_data PASSED                                                                                          [ 21%]
tests/test_comments/test_delete_comment.py::TestCommentResource::test_delete_comment_with_invalid_task PASSED                                                                                        [ 28%]
tests/test_comments/test_delete_comment.py::TestCommentResource::test_delete_comment_with_invalid_comment PASSED                                                                                     [ 35%]
tests/test_comments/test_fetch_comments.py::TestCommentResource::test_get_comments_for_task PASSED                                                                                                   [ 42%]
tests/test_comments/test_fetch_comments.py::TestCommentResource::test_get_comments_for_invalid_task PASSED                                                                                           [ 50%]
tests/test_comments/test_update_comment.py::TestCommentResource::test_update_comment_with_valid_data PASSED                                                                                          [ 57%]
tests/test_comments/test_update_comment.py::TestCommentResource::test_update_comment_with_invalid_task PASSED                                                                                        [ 64%]
tests/test_comments/test_update_comment.py::TestCommentResource::test_update_comment_with_invalid_comment PASSED                                                                                     [ 71%]
tests/test_signin/test_signin.py::TestSigninResource::test_successful_user_login PASSED                                                                                                              [ 78%]
tests/test_signin/test_signin.py::TestSigninResource::test_user_login_failure PASSED                                                                                                                 [ 85%]
tests/test_signup/test_signup.py::TestSignupResource::test_user_registration_with_valid_data_and_default_role PASSED                                                                                 [ 92%]
tests/test_signup/test_signup.py::TestSignupResource::test_user_registration_with_existing_email PASSED                                                                                              [100%]

============================================================================================ 14 passed in 0.98s ============================================================================================
```

4- Generate and view report

`coverage html && open htmlcov/index.html
coverage xml
`
Current coverage is **82%** and report can be found at [index.html](https://github.com/tubahashmi/task_manager_api/blob/main/tests/index.html)