from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class TrafficState(Base):
    __tablename__ = "traffic_states"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    junction_id: Mapped[str] = mapped_column(String(2), index=True)
    vehicle_count: Mapped[int] = mapped_column(Integer)
    average_speed: Mapped[float] = mapped_column(Float)
    queue_length: Mapped[float] = mapped_column(Float)
    density: Mapped[float] = mapped_column(Float)
    traffic_flow: Mapped[float] = mapped_column(Float)
    movement_utilization: Mapped[float] = mapped_column(Float)
    congestion_score: Mapped[float] = mapped_column(Float)
    congestion_category: Mapped[str] = mapped_column(String(12))
    weather: Mapped[str] = mapped_column(String(12))
