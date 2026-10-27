"""add table check constraints

Revision ID: 7765e89e79c4
Revises: 09245ef7c736
Create Date: 2026-10-27 13:04:08.919206

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7765e89e79c4'
down_revision = '09245ef7c736'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('exercises') as batch_op:
        batch_op.create_check_constraint(
            'ck_exercises_valid_category',
            "category IN ('Cardio', 'Strength', 'Flexibility', 'HIIT')",
        )

    with op.batch_alter_table('workouts') as batch_op:
        batch_op.create_check_constraint(
            'ck_workouts_positive_duration',
            'duration_minutes > 0',
        )

    with op.batch_alter_table('workout_exercises') as batch_op:
        batch_op.create_check_constraint(
            'ck_workout_exercises_positive_sets',
            'sets > 0',
        )
        batch_op.create_check_constraint(
            'ck_workout_exercises_positive_reps',
            'reps IS NULL OR reps > 0',
        )


def downgrade():
    with op.batch_alter_table('workout_exercises') as batch_op:
        batch_op.drop_constraint(
            'ck_workout_exercises_positive_reps',
            type_='check',
        )
        batch_op.drop_constraint(
            'ck_workout_exercises_positive_sets',
            type_='check',
        )

    with op.batch_alter_table('workouts') as batch_op:
        batch_op.drop_constraint(
            'ck_workouts_positive_duration',
            type_='check',
        )

    with op.batch_alter_table('exercises') as batch_op:
        batch_op.drop_constraint(
            'ck_exercises_valid_category',
            type_='check',
        )
