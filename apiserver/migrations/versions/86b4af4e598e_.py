#!./venv/bin/python
# -*- coding: utf-8 -*-

"""empty message

Revision ID: 86b4af4e598e
Create Date: 2023-04-04 09:31:25.673260

"""

# pylint: disable=C0103,C0116,E1101

# Third-party
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '86b4af4e598e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'roles',
        sa.Column('id', sa.INTEGER, nullable=False, autoincrement=True,),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    op.drop_table('roles')
    # ### end Alembic commands ###
