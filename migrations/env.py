from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Base


# this will use the URL from alembic.ini
config = context.config

# importing your Base
from models import Base
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()
def upgrade():
    # Create concerts table
    op.create_table('concerts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('date', sa.String(), nullable=False),
        sa.Column('band_id', sa.Integer(), sa.ForeignKey('bands.id')),
        sa.Column('venue_id', sa.Integer(), sa.ForeignKey('venues.id'))
    )

def downgrade():
    op.drop_table('concerts')
