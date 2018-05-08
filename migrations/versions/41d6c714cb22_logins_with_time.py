"""logins with time

Revision ID: 41d6c714cb22
Revises: 1eec94e3a38d
Create Date: 2018-05-03 12:55:10.602370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41d6c714cb22'
down_revision = '1eec94e3a38d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('logins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('timestamp', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_logins_timestamp'), ['timestamp'], unique=False)
        batch_op.drop_column('title')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('logins', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.INTEGER(), nullable=True))
        batch_op.drop_index(batch_op.f('ix_logins_timestamp'))
        batch_op.drop_column('timestamp')

    # ### end Alembic commands ###