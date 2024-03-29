"""initial

Revision ID: 67f37bbcd848
Revises: 
Create Date: 2024-03-26 15:00:25.018149

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "67f37bbcd848"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "user_data",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.BigInteger),
        sa.Column("timestamp", sa.DateTime),
        sa.Column("chat_id", sa.BigInteger),
        sa.Column("prompt_text", sa.String),
    )


def downgrade():
    op.drop_table("user_data")
