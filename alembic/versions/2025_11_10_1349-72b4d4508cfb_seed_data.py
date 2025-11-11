"""seed data

Revision ID: 72b4d4508cfb
Revises: dc9abbb0480b
Create Date: 2025-11-10 13:49:25.081614

"""

import json
from pathlib import Path
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from app.models.incident import IncidentStatus, IncidentSource


# revision identifiers, used by Alembic.
revision: str = "72b4d4508cfb"
down_revision: Union[str, Sequence[str], None] = "dc9abbb0480b"
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

    # --- Загрузка статусов ---
    status_objs = [IncidentStatus(**item) for item in data["incident_status"]]
    session.bulk_save_objects(status_objs)

    # --- Загрузка источников ---
    source_objs = [IncidentSource(**item) for item in data["incident_source"]]
    session.bulk_save_objects(source_objs)

    session.commit()
    print("Seed data загружено!")


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    # Удаляем в обратном порядке
    session.query(IncidentSource).delete()
    session.query(IncidentStatus).delete()
    session.commit()
    print("Seed data удалено!")
