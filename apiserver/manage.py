#!./venv/bin/python
# -*- coding: utf-8 -*-

"""Management script to run commands within application context."""

# pylint: disable=R0401

# Third-party
import click
from flask.cli import with_appcontext

# First-party
from apiserver.extensions import db


@click.command()
@with_appcontext
def init():
    """Initializes by dropping all collections and creating fresh."""
    db.drop_all()
    db.create_all()
