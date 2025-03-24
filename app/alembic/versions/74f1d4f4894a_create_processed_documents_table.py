"""Create processed_documents table

Revision ID: 74f1d4f4894a
Revises: 
Create Date: 2025-03-20 10:50:43.442472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '74f1d4f4894a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.dialects import postgresql

def upgrade():
  
    documentsclassifcation = postgresql.ENUM(
        'PENDING', 'PROCESSING', 'PROCESSED', 'FAILED',
        name='documentsclassifcation',
        create_type=True
    )


    op.create_table('processed_documents',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('filename', sa.String(length=255), nullable=False, unique=True),  
        sa.Column('checksum', sa.String(length=64)), 
        sa.Column('status', documentsclassifcation, nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()')),
        
        sa.UniqueConstraint('checksum', name='uq_processed_documents_checksum')
    )

def downgrade():
    op.drop_table('processed_documents')
    
    op.execute("DROP TYPE IF EXISTS documentstatus CASCADE")