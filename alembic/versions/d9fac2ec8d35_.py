"""

Revision ID: d9fac2ec8d35
Revises: 47bb2307018b
Create Date: 2021-05-16 16:40:16.312493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9fac2ec8d35'
down_revision = '47bb2307018b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_segments_geometry', table_name='segments')
    op.create_index(op.f('ix_subsegments_non_parking_segment_id'), 'subsegments_non_parking', ['segment_id'], unique=False)
    op.create_index(op.f('ix_subsegments_parking_segment_id'), 'subsegments_parking', ['segment_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_subsegments_parking_segment_id'), table_name='subsegments_parking')
    op.drop_index(op.f('ix_subsegments_non_parking_segment_id'), table_name='subsegments_non_parking')
    op.create_index('idx_segments_geometry', 'segments', ['geometry'], unique=False)
    # ### end Alembic commands ###
