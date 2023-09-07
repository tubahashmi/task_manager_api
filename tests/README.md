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

4- Generate and view report

`coverage html && open htmlcov/index.html
coverage xml
`