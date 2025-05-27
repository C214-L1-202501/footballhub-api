from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from app.schemas.country import Country


class Stadium(SQLModel, table=True):
    __tablename__ = "stadiums"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    city: str = Field(max_length=100, nullable=False)
    country_id: int = Field(foreign_key="countries.id", nullable=False)
    country: Optional["Country"] = Relationship(back_populates="stadiums")