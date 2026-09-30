from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.session import Base


class Junction(Base):
    __tablename__ = "junctions"

    id: Mapped[int] = mapped_column(primary_key=True)
    junction_id: Mapped[str] = mapped_column(String(2), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(80))
    status: Mapped[str] = mapped_column(String(30), default="awaiting_demo_data")
