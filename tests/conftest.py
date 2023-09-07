from unittest.mock import patch

import pytest

from apiserver.app import create_app
from tests.config import TestingConfig


@pytest.yield_fixture
def app():
    """Flask Test App"""
    with patch('flask_sqlalchemy.SQLAlchemy'):
        with patch('apiserver.extensions.db'):
            app = create_app()
            app.config['TESTING'] = True
            app.config['SQLALCHEMY_DATABASE_URI'] = None
            app.config.from_object(TestingConfig)
            ctx = app.test_request_context()
            ctx.push()
            yield app
            ctx.pop()