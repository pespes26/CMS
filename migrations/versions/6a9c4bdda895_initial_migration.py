"""Initial migration

Revision ID: 6a9c4bdda895
Revises: 
Create Date: 2024-08-31 13:19:19.345893

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6a9c4bdda895'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.drop_constraint('lecture_time_course_id_fkey', 'lecture_time', type_='foreignkey')
    op.drop_constraint('practice_time_course_id_fkey', 'practice_time', type_='foreignkey')
    op.drop_table('lecture_time')
    op.drop_table('practice_time')
    op.drop_table('course')

    # Recreate the course table with the corrected column name
    op.create_table(
        'course',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('courseid', sa.String(50), nullable=False),  # Note the lowercase
    )

    # Recreate the lecture_time table with correct references
    op.create_table(
        'lecture_time',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('day', sa.String(length=50), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('building', sa.String(length=10), nullable=False),
        sa.Column('classroom', sa.String(length=10), nullable=False),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('course.id', ondelete='CASCADE'))
    )

    # Recreate the practice_time table with correct references
    op.create_table(
        'practice_time',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('day', sa.String(length=50), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('building', sa.String(length=10), nullable=False),
        sa.Column('classroom', sa.String(length=10), nullable=False),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('course.id', ondelete='CASCADE'))
    )

def downgrade():
    # Commands to reverse the migration, creating the tables again if the upgrade is undone
    op.drop_constraint('lecture_time_course_id_fkey', 'lecture_time', type_='foreignkey')
    op.drop_constraint('practice_time_course_id_fkey', 'practice_time', type_='foreignkey')
    op.drop_table('lecture_time')
    op.drop_table('practice_time')
    op.drop_table('course')

