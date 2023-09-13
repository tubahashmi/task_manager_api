#!./venv/bin/python
# -*- coding: utf-8 -*-

""" Added for DEBUGGING purpose from pycharm, otherwise we can run it through cli
    ../apiserver$ flask run -h 0.0.0.0 """

# First-party
from apiserver.app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost')
