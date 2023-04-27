"""num

Revision ID: da53bcbc0c67
Revises: 5643ed8cb30b
Create Date: 2023-04-26 11:51:48.282013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da53bcbc0c67'
down_revision = '5643ed8cb30b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('model_next',
    sa.Column('name', sa.VARCHAR(length=128), nullable=False),
    sa.Column('model_id', sa.SmallInteger(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['model_id'], ['models.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('model_next')
    # ### end Alembic commands ###
