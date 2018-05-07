"""1

Revision ID: 7500806ebff3
Revises: 5db3e0b8f801
Create Date: 2018-05-02 12:52:07.855781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7500806ebff3'
down_revision = '5db3e0b8f801'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blogpost', schema=None) as batch_op:
        batch_op.drop_column('editor_id')

    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_messages_date_posted'), ['date_posted'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_messages_date_posted'))

    with op.batch_alter_table('blogpost', schema=None) as batch_op:
        batch_op.add_column(sa.Column('editor_id', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
