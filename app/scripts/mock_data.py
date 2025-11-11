import json
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models import Incident, IncidentSource, IncidentStatus

BASE_DIR = Path(__file__).resolve().parent

SEED_DATA_PATH = BASE_DIR / "mock_data.json"
print(SEED_DATA_PATH)
Session = sessionmaker()

engine = create_engine(settings.db.sync_url)


def add_mock_data():
    session = Session(bind=engine)

    with open(SEED_DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    status_objs = [IncidentStatus(**item) for item in data["incident_status"]]
    session.bulk_save_objects(status_objs)

    source_objs = [IncidentSource(**item) for item in data["incident_source"]]
    session.bulk_save_objects(source_objs)

    status_objs = [Incident(**item) for item in data["incidents"]]
    session.bulk_save_objects(status_objs)

    session.commit()

    return {"status": "success", "message": "Данные успешно добавлены."}


def delete_mock_data():
    session = Session(bind=engine)

    session.query(Incident).delete()
    session.query(IncidentSource).delete()
    session.query(IncidentStatus).delete()

    session.commit()

    return {"status": "success", "message": "Данные успешно удалены."}
