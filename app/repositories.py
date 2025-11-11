from typing import List, Sequence, AsyncGenerator, Optional

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.core.db import get_session
from app.models.incident import Incident, IncidentStatus, IncidentSource
from app.schemas.incident import IncidentCreate


def get_incident_repo(session: AsyncSession = Depends(get_session)):
    return IncidentRepository(session)


class IncidentRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_incidents(
        self, status_id: Optional[int] = None, skip: int = 0, limit: int = 100
    ) -> Sequence[Incident]:
        stmt = (
            select(Incident)
            .options(joinedload(Incident.status), joinedload(Incident.source))
            .offset(skip)
            .limit(limit)
            .order_by(Incident.created_at.desc())
        )
        if status_id is not None:
            stmt = stmt.where(Incident.status_id == status_id)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create_incident(self, incident_in: IncidentCreate):
        status = await self._session.get(IncidentStatus, incident_in.status_id)
        if not status:
            raise HTTPException(status_code=400, detail="Incident status not found")

        source = await self._session.get(IncidentSource, incident_in.source_id)
        if not source:
            raise HTTPException(status_code=400, detail="Incident source not found")

        incident = Incident(
            description=incident_in.description,
            status_id=incident_in.status_id,
            source_id=incident_in.source_id,
        )

        self._session.add(incident)
        await self._session.commit()
        await self._session.refresh(incident)

        result = await self._session.execute(
            select(Incident)
            .options(joinedload(Incident.status), joinedload(Incident.source))
            .where(Incident.id == incident.id)
        )
        return result.scalars().one()

    async def update_incident(self, incident_id: int, status_id: int) -> Incident:
        incident = await self._session.get(Incident, incident_id)
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")

        new_status = await self._session.get(IncidentStatus, status_id)
        if not new_status:
            raise HTTPException(status_code=404, detail="Incident status not found")

        incident.status_id = status_id
        await self._session.commit()
        await self._session.refresh(incident)

        stmt = (
            select(Incident)
            .options(joinedload(Incident.status), joinedload(Incident.source))
            .where(Incident.id == incident_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def get_statuses(self) -> Sequence[IncidentStatus]:
        stmt = select(IncidentStatus).order_by(IncidentStatus.id)
        result = await self._session.execute(stmt)
        return result.scalars().all()
