"""add applications for operators

Revision ID: 7c6d90394650
Revises: ae1d6fd2c907
Create Date: 2023-04-23 19:58:38.898864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c6d90394650'
down_revision = 'ae1d6fd2c907'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.String(length=300), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('apartment', sa.String(length=200), nullable=False),
    sa.Column('master_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('image', sa.String(length=300), nullable=False),
    sa.Column('problem', sa.String(length=3000), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['master_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application_report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('application_id', sa.Integer(), nullable=False),
    sa.Column('master_id', sa.Integer(), nullable=False),
    sa.Column('addition', sa.String(length=3000), nullable=False),
    sa.Column('image', sa.String(length=300), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.ForeignKeyConstraint(['application_id'], ['application.id'], ),
    sa.ForeignKeyConstraint(['master_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('application_report')
    op.drop_table('application')
    op.drop_table('application_status')
    # ### end Alembic commands ###
