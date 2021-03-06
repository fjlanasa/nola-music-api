"""empty message

Revision ID: 733ab7b32c34
Revises: 236d4ece9dde
Create Date: 2018-01-24 10:37:14.678927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '733ab7b32c34'
down_revision = '236d4ece9dde'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artists', sa.Column('preview_video_thumbnail', sa.String(length=140), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artists', 'preview_video_thumbnail')
    # ### end Alembic commands ###
