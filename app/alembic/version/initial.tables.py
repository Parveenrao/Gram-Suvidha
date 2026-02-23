"""Initial tables — create all tables

Revision ID: 001
Revises: 
Create Date: 2024-02-20

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ── 1. villages ──────────────────────────────
    op.create_table(
        'villages',
        sa.Column('id',         sa.Integer(),                  nullable=False),
        sa.Column('name',       sa.String(),                   nullable=False),
        sa.Column('district',   sa.String(),                   nullable=False),
        sa.Column('state',      sa.String(),                   nullable=False),
        sa.Column('pincode',    sa.String(),                   nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),    server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_villages_id', 'villages', ['id'])

    # ── 2. users ─────────────────────────────────
    op.create_table(
        'users',
        sa.Column('id',               sa.Integer(),  nullable=False),
        sa.Column('full_name',        sa.String(),   nullable=False),
        sa.Column('phone',            sa.String(),   nullable=False),
        sa.Column('email',            sa.String(),   nullable=True),
        sa.Column('hashed_password',  sa.String(),   nullable=False),
        sa.Column('role',
            sa.Enum('admin', 'sarpanch', 'ward_member', 'citizen',
                    name='roleenum'),
            nullable=True
        ),
        sa.Column('ward_number',  sa.Integer(),              nullable=True),
        sa.Column('village_id',   sa.Integer(),              nullable=False),
        sa.Column('is_active',    sa.Boolean(),              default=True),
        sa.Column('created_at',   sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['village_id'], ['villages.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('phone'),
        sa.UniqueConstraint('email')
    )
    op.create_index('ix_users_id', 'users', ['id'])

    # ── 3. budgets ───────────────────────────────
    op.create_table(
        'budgets',
        sa.Column('id',              sa.Integer(),              nullable=False),
        sa.Column('village_id',      sa.Integer(),              nullable=False),
        sa.Column('financial_year',  sa.String(),               nullable=False),
        sa.Column('total_allocated', sa.Float(),                nullable=False),
        sa.Column('total_spent',     sa.Float(),                default=0.0),
        sa.Column('description',     sa.String(),               nullable=True),
        sa.Column('created_at',      sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['village_id'], ['villages.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_budgets_id', 'budgets', ['id'])

    # ── 4. budget_transactions ───────────────────
    op.create_table(
        'budget_transactions',
        sa.Column('id',        sa.Integer(), nullable=False),
        sa.Column('budget_id', sa.Integer(), nullable=False),
        sa.Column('category',
            sa.Enum('road', 'water', 'sanitation', 'education',
                    'health', 'electricity', 'agriculture', 'other',
                    name='categoryenum'),
            nullable=False
        ),
        sa.Column('amount',      sa.Float(),                nullable=False),
        sa.Column('description', sa.String(),               nullable=False),
        sa.Column('spent_by',    sa.Integer(),              nullable=True),
        sa.Column('date',        sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['budget_id'], ['budgets.id']),
        sa.ForeignKeyConstraint(['spent_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_budget_transactions_id', 'budget_transactions', ['id'])

    # ── 5. projects ──────────────────────────────
    op.create_table(
        'projects',
        sa.Column('id',             sa.Integer(), nullable=False),
        sa.Column('village_id',     sa.Integer(), nullable=False),
        sa.Column('title',          sa.String(),  nullable=False),
        sa.Column('description',    sa.String(),  nullable=True),
        sa.Column('category',       sa.String(),  nullable=False),
        sa.Column('ward_number',    sa.Integer(), nullable=True),
        sa.Column('estimated_cost', sa.Float(),   nullable=False),
        sa.Column('actual_cost',    sa.Float(),   default=0.0),
        sa.Column('status',
            sa.Enum('planned', 'ongoing', 'completed', 'cancelled',
                    name='projectstatusenum'),
            default='planned'
        ),
        sa.Column('start_date',  sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_date',    sa.DateTime(timezone=True), nullable=True),
        sa.Column('photos',      sa.JSON(),                  default=list),
        sa.Column('created_by',  sa.Integer(),               nullable=True),
        sa.Column('created_at',  sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at',  sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['village_id'], ['villages.id']),
        sa.ForeignKeyConstraint(['created_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_projects_id', 'projects', ['id'])

    # ── 6. announcements ─────────────────────────
    op.create_table(
        'announcements',
        sa.Column('id',           sa.Integer(), nullable=False),
        sa.Column('village_id',   sa.Integer(), nullable=False),
        sa.Column('title',        sa.String(),  nullable=False),
        sa.Column('content',      sa.String(),  nullable=False),
        sa.Column('type',
            sa.Enum('notice', 'scheme', 'meeting', 'alert', 'general',
                    name='announcementtypeenum'),
            default='general'
        ),
        sa.Column('published_by', sa.Integer(),              nullable=True),
        sa.Column('created_at',   sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['village_id'],   ['villages.id']),
        sa.ForeignKeyConstraint(['published_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_announcements_id', 'announcements', ['id'])

    # ── 7. grievances ────────────────────────────
    op.create_table(
        'grievances',
        sa.Column('id',             sa.Integer(), nullable=False),
        sa.Column('village_id',     sa.Integer(), nullable=False),
        sa.Column('citizen_id',     sa.Integer(), nullable=False),
        sa.Column('title',          sa.String(),  nullable=False),
        sa.Column('description',    sa.String(),  nullable=False),
        sa.Column('category',       sa.String(),  nullable=False),
        sa.Column('status',
            sa.Enum('open', 'in_progress', 'resolved', 'rejected',
                    name='grievancestatusenum'),
            default='open'
        ),
        sa.Column('sarpanch_reply', sa.String(),              nullable=True),
        sa.Column('created_at',     sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('resolved_at',    sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['village_id'], ['villages.id']),
        sa.ForeignKeyConstraint(['citizen_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_grievances_id', 'grievances', ['id'])

    # ── 8. documents ─────────────────────────────
    op.create_table(
        'documents',
        sa.Column('id',          sa.Integer(), nullable=False),
        sa.Column('village_id',  sa.Integer(), nullable=False),
        sa.Column('title',       sa.String(),  nullable=False),
        sa.Column('file_url',    sa.String(),  nullable=False),
        sa.Column('type',
            sa.Enum('certificate', 'notice', 'budget_report',
                    'meeting_minutes', 'other',
                    name='documenttypeenum'),
            default='other'
        ),
        sa.Column('uploaded_by', sa.Integer(),              nullable=True),
        sa.Column('created_at',  sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['village_id'],  ['villages.id']),
        sa.ForeignKeyConstraint(['uploaded_by'], ['users.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_documents_id', 'documents', ['id'])


def downgrade() -> None:
    """Drop all tables in reverse order."""

    # drop tables first
    op.drop_table('documents')
    op.drop_table('grievances')
    op.drop_table('announcements')
    op.drop_table('projects')
    op.drop_table('budget_transactions')
    op.drop_table('budgets')
    op.drop_table('users')
    op.drop_table('villages')

    # drop all enums
    op.execute('DROP TYPE IF EXISTS documenttypeenum')
    op.execute('DROP TYPE IF EXISTS grievancestatusenum')
    op.execute('DROP TYPE IF EXISTS announcementtypeenum')
    op.execute('DROP TYPE IF EXISTS projectstatusenum')
    op.execute('DROP TYPE IF EXISTS categoryenum')
    op.execute('DROP TYPE IF EXISTS roleenum')