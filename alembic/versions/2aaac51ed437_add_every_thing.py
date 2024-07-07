"""add every thing

Revision ID: 2aaac51ed437
Revises: 
Create Date: 2024-07-07 00:43:01.725555

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision = '2aaac51ed437'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users", sa.Column("id", sa.Integer() , nullable = False, primary_key = True), sa.Column("name", sa.String(), nullable = False, unique = True), sa.Column("password", sa.String(), nullable = False), sa.Column("user_character", sa.String(), nullable = False), sa.Column("coins", sa.Integer(), nullable = False, server_default = '0'), sa.Column("shown_films", sa.ARRAY(sa.Integer), nullable = False, server_default = "{}"), sa.Column("created_at", sa.TIMESTAMP(timezone= True), nullable = False, server_default = text('now()')))

    op.create_table("bloodyfilm", sa.Column("id", sa.Integer(), nullable = False, primary_key = True), sa.Column("type", sa.String, server_default = 'bloody film'), sa.Column("title", sa.String, server_default = f'bloody film number {id}', nullable = False), sa.Column("description", sa.String, nullable = False), sa.Column("video_url", sa.Integer, nullable = False), sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable = True, server_default = text('now()')))
    pass


def downgrade():
    pass
