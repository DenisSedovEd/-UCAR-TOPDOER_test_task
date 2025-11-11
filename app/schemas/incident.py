from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IncidentStatusSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class IncidentSourceSchema(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class IncidentBase(BaseModel):
    description: str
    source_id: int
    status_id: int


class IncidentCreate(IncidentBase):
    status_id: int
    source_id: int


class IncidentResponse(IncidentBase):
    id: int
    created_at: datetime
    status: IncidentStatusSchema
    source: IncidentSourceSchema

    class Config:
        from_attributes = True
