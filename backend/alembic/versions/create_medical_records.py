"""create medical records table

Revision ID: create_medical_records
Revises: 
Create Date: 2024-12-30

"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('medical_records',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('patient_id', sa.Integer(), nullable=False),
        sa.Column('visit_date', sa.DateTime(), nullable=False),
        sa.Column('chief_complaint', sa.Text(), nullable=True),
        sa.Column('history', sa.Text(), nullable=True),
        sa.Column('examination', sa.Text(), nullable=True),
        sa.Column('diagnosis', sa.Text(), nullable=True),
        sa.Column('plan', sa.Text(), nullable=True),
        sa.Column('transcription', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_medical_records_id'), 'medical_records', ['id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_medical_records_id'), table_name='medical_records')
    op.drop_table('medical_records')