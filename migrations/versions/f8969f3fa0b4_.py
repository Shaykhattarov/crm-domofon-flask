"""empty message

Revision ID: f8969f3fa0b4
Revises: 623a665b24dc
Create Date: 2023-05-17 16:18:15.045925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8969f3fa0b4'
down_revision = '623a665b24dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.drop_constraint('application_ibfk_4', type_='foreignkey')
        batch_op.drop_constraint('application_ibfk_5', type_='foreignkey')
        batch_op.create_foreign_key(None, 'application_status', ['status'], ['id'])
        batch_op.create_foreign_key(None, 'address', ['address_id'], ['id'])

    with op.batch_alter_table('application_report', schema=None) as batch_op:
        batch_op.drop_constraint('application_report_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'application', ['application_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('application_report', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('application_report_ibfk_3', 'application', ['application_id'], ['id'], onupdate='RESTRICT', ondelete='CASCADE')

    with op.batch_alter_table('application', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('application_ibfk_5', 'application_status', ['status'], ['id'], onupdate='RESTRICT', ondelete='CASCADE')
        batch_op.create_foreign_key('application_ibfk_4', 'address', ['address_id'], ['id'], ondelete='CASCADE')

    # ### end Alembic commands ###
