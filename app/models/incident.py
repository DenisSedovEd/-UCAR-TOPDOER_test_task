from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class IncidentStatus(Base):
    __tablename__ = "incident_status"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    incidents: Mapped["Incident"] = relationship(
        "Incident",
        back_populates="status",
    )


class IncidentSource(Base):
    __tablename__ = "incident_source"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )
    incidents: Mapped["Incident"] = relationship(
        "Incident",
        back_populates="source",
    )


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        String(1000),
    )

    status_id: Mapped[int] = mapped_column(
        ForeignKey("incident_status.id", ondelete="SET NULL"),
        nullable=False,
        index=True,
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey("incident_source.id", ondelete="SET NULL"),
        nullable=False,
        index=True,
    )
    status: Mapped[IncidentStatus] = relationship(
        "IncidentStatus",
        back_populates="incidents",
    )
    source: Mapped[IncidentSource] = relationship(
        "IncidentSource",
        back_populates="incidents",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
