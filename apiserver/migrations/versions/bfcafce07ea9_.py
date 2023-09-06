#!./venv/bin/python
# -*- coding: utf-8 -*-

"""empty message

Revision ID: bfcafce07ea9
Revises: 86b4af4e598e
Create Date: 2023-09-05 01:55:18.008826

"""

# pylint: disable=C0103,C0116,E1101

# Third-party
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bfcafce07ea9'
down_revision = '86b4af4e598e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('first_name', sa.String(length=50), nullable=True),
        sa.Column('last_name', sa.String(length=50), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('password', sa.String(length=128), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['role_id'],
            ['roles.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('id'),
    )
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.alter_column(
            'name',
            existing_type=mysql.VARCHAR(length=50),
            type_=sa.String(length=20),
            existing_nullable=False,
        )
        batch_op.create_unique_constraint(None, ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('roles', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column(
            'name',
            existing_type=sa.String(length=20),
            type_=mysql.VARCHAR(length=50),
            existing_nullable=False,
        )

    op.drop_table('users')
    # ### end Alembic commands ###