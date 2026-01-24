"""initial table schemas

Revision ID: 39b3251386c7
Revises: 
Create Date: 2026-01-24 23:50:52.194190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39b3251386c7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('brands',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('tier', sa.Enum('TOP', 'MIDDLE', 'LOW', name='tierenum'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('categories',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('is_limited', sa.Boolean(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shops',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.Column('ships_to_czech', sa.Boolean(), nullable=False),
    sa.Column('shipping_fee', sa.Float(), nullable=True),
    sa.Column('other_fees', sa.Float(), nullable=True),
    sa.Column('free_shipping_from_price', sa.Float(), nullable=False),
    sa.Column('is_in_eu_market', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('models',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('brand_id', sa.UUID(), nullable=False),
    sa.Column('model_id', sa.String(), nullable=True),
    sa.Column('car_brand', sa.String(), nullable=False),
    sa.Column('category_id', sa.UUID(), nullable=False),
    sa.Column('has_chase_version', sa.Boolean(), nullable=False),
    sa.Column('release_year', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brands.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('customer_models',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('model_id', sa.UUID(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('condition', sa.Enum('NEW', 'UNPACKED', 'USED', 'DAMAGED', name='conditionenum'), nullable=False),
    sa.ForeignKeyConstraint(['model_id'], ['models.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shop_products',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('shop_id', sa.UUID(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('currency', sa.String(), nullable=False),
    sa.Column('price_in_czk', sa.Float(), nullable=False),
    sa.Column('conversion_rate', sa.Float(), nullable=False),
    sa.Column('model_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
    sa.Column('original_name', sa.String(), nullable=False),
    sa.Column('is_last', sa.Boolean(), nullable=False),
    sa.Column('condition', sa.Enum('NEW', 'UNPACKED', 'USED', 'DAMAGED', name='conditionenum'), nullable=False),
    sa.Column('packaging', sa.Enum('BOX', 'BLISTER', 'WITHOUT', name='packageenum'), nullable=False),
    sa.ForeignKeyConstraint(['model_id'], ['models.id'], ),
    sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('shop_products')
    op.drop_table('customer_models')
    op.drop_table('models')
    op.drop_table('shops')
    op.drop_table('customers')
    op.drop_table('categories')
    op.drop_table('brands')
    
    # Drop enums after dropping tables
    op.execute('DROP TYPE IF EXISTS packageenum')
    op.execute('DROP TYPE IF EXISTS conditionenum')
    op.execute('DROP TYPE IF EXISTS tierenum')
