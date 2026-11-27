"""Initial schema - create all tables.

Revision ID: 001
Revises:
Create Date: 2026-11-26
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role', sa.Enum('coach', 'admin', name='userrole'), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # teams
    op.create_table(
        'teams',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('coach_id', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['coach_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_teams_id'), 'teams', ['id'], unique=False)

    # athletes
    op.create_table(
        'athletes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('birth_date', sa.Date(), nullable=False),
        sa.Column('position', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_athletes_id'), 'athletes', ['id'], unique=False)
    op.create_index(op.f('ix_athletes_team_id'), 'athletes', ['team_id'], unique=False)

    # trainings
    op.create_table(
        'trainings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('team_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('theme', sa.String(length=200), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_trainings_id'), 'trainings', ['id'], unique=False)
    op.create_index(op.f('ix_trainings_team_id'), 'trainings', ['team_id'], unique=False)
    op.create_index(op.f('ix_trainings_date'), 'trainings', ['date'], unique=False)

    # attendances
    op.create_table(
        'attendances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('training_id', sa.Integer(), nullable=False),
        sa.Column('athlete_id', sa.Integer(), nullable=False),
        sa.Column('present', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['training_id'], ['trainings.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['athlete_id'], ['athletes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('training_id', 'athlete_id', name='uq_attendance_training_athlete'),
    )
    op.create_index(op.f('ix_attendances_id'), 'attendances', ['id'], unique=False)
    op.create_index(op.f('ix_attendances_training_id'), 'attendances', ['training_id'], unique=False)
    op.create_index(op.f('ix_attendances_athlete_id'), 'attendances', ['athlete_id'], unique=False)

    # evaluations
    op.create_table(
        'evaluations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('athlete_id', sa.Integer(), nullable=False),
        sa.Column('evaluator_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('pass_rating', sa.Integer(), nullable=False),
        sa.Column('serve_rating', sa.Integer(), nullable=False),
        sa.Column('attack_rating', sa.Integer(), nullable=False),
        sa.Column('block_rating', sa.Integer(), nullable=False),
        sa.Column('defense_rating', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['athlete_id'], ['athletes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['evaluator_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('pass_rating BETWEEN 1 AND 5', name='ck_pass_rating_range'),
        sa.CheckConstraint('serve_rating BETWEEN 1 AND 5', name='ck_serve_rating_range'),
        sa.CheckConstraint('attack_rating BETWEEN 1 AND 5', name='ck_attack_rating_range'),
        sa.CheckConstraint('block_rating BETWEEN 1 AND 5', name='ck_block_rating_range'),
        sa.CheckConstraint('defense_rating BETWEEN 1 AND 5', name='ck_defense_rating_range'),
    )
    op.create_index(op.f('ix_evaluations_id'), 'evaluations', ['id'], unique=False)
    op.create_index(op.f('ix_evaluations_athlete_id'), 'evaluations', ['athlete_id'], unique=False)
    op.create_index(op.f('ix_evaluations_evaluator_id'), 'evaluations', ['evaluator_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_evaluations_evaluator_id'), table_name='evaluations')
    op.drop_index(op.f('ix_evaluations_athlete_id'), table_name='evaluations')
    op.drop_index(op.f('ix_evaluations_id'), table_name='evaluations')
    op.drop_table('evaluations')

    op.drop_index(op.f('ix_attendances_athlete_id'), table_name='attendances')
    op.drop_index(op.f('ix_attendances_training_id'), table_name='attendances')
    op.drop_index(op.f('ix_attendances_id'), table_name='attendances')
    op.drop_table('attendances')

    op.drop_index(op.f('ix_trainings_date'), table_name='trainings')
    op.drop_index(op.f('ix_trainings_team_id'), table_name='trainings')
    op.drop_index(op.f('ix_trainings_id'), table_name='trainings')
    op.drop_table('trainings')

    op.drop_index(op.f('ix_athletes_team_id'), table_name='athletes')
    op.drop_index(op.f('ix_athletes_id'), table_name='athletes')
    op.drop_table('athletes')

    op.drop_index(op.f('ix_teams_id'), table_name='teams')
    op.drop_table('teams')

    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    # Drop enum type
    op.execute("DROP TYPE IF EXISTS userrole")