from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, JSON, Date
from typing import List
from datetime import date


class Base(DeclarativeBase):
    pass


class Vacancy(Base):
    __tablename__ = "Vacancies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    hh_id: Mapped[str] = mapped_column(String(30), unique=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    skills: Mapped[List[str]] = mapped_column(JSON)
    published_at: Mapped[date] = mapped_column(Date)
    work_format: Mapped[str] = mapped_column(String(50))
    url: Mapped[str] = mapped_column(String(512))
