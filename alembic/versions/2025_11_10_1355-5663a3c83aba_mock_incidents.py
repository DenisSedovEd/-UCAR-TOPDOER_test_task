"""mock incidents

Revision ID: 5663a3c83aba
Revises: 72b4d4508cfb
Create Date: 2025-11-10 13:55:58.996631

"""

import json
from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from app.models.incident import Incident

# revision identifiers, used by Alembic.
revision: str = "5663a3c83aba"
down_revision: Union[str, Sequence[str], None] = "72b4d4508cfb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


BASE_DIR = Path(__file__).resolve().parent.parent.parent
SEED_DATA_PATH = BASE_DIR / "seed_data" / "seed_data.json"
Session = sessionmaker()


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    with open(SEED_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- Загрузка инцидентов ---
    status_objs = [Incident(**item) for item in data["incidents"]]
    session.bulk_save_objects(status_objs)

    session.commit()
    print("Seed data загружено!")


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    # Удаляем
    session.query(Incident).delete()
    session.commit()
    print("Seed data удалено!")
