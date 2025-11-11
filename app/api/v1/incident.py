from typing import List, Optional

from fastapi import APIRouter, Query
from fastapi.params import Depends

from app.schemas.incident import IncidentResponse, IncidentStatusSchema
from app.models.incident import Incident
from app.repositories import IncidentRepository, get_incident_repo
from app.schemas.incident import IncidentCreate

router = APIRouter(prefix="/incidents", tags=["incident"])


@router.get("/", response_model=List[IncidentResponse])
async def get_incidents(
    status_id: Optional[int] = Query(None, description="Filter by status ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=10, le=100),
    repo: IncidentRepository = Depends(get_incident_repo),
):
    incidents = await repo.get_incidents(status_id, skip, limit)
    return incidents


@router.post("/incident", response_model=IncidentCreate)
async def create_incident(
    incident_in: IncidentCreate, repo: IncidentRepository = Depends(get_incident_repo)
) -> IncidentResponse:
    incident = await repo.create_incident(incident_in)
    return IncidentResponse.model_validate(incident)


@router.patch(("/incident/{incident_id}"), response_model=IncidentResponse)
async def update_incident(
    incident_id: int,
    status_id: int,
    repo: IncidentRepository = Depends(get_incident_repo),
):
    incident = await repo.update_incident(incident_id, status_id)
    return IncidentResponse.model_validate(incident)


@router.get("/statuses_incident", response_model=List[IncidentStatusSchema])
async def get_incidents_statuses(repo: IncidentRepository = Depends(get_incident_repo)):
    incidents_statuses = await repo.get_statuses()
    return incidents_statuses
