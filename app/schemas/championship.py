from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from app.schemas.country import Country


class Championship(SQLModel, table=True):
    """Championship object."""
    __tablename__ = "championships"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    country_id: Optional[int] = Field(default=None, foreign_key="country.id")
    type: Optional[str] = Field(max_length=50, default=None)
    season: Optional[str] = Field(max_length=20, default=None)

    country: Optional["Country"] = Relationship(back_populates="championships")


Country.championships = Relationship(
    back_populates="country", sa_relationship_kwargs={"lazy": "selectin"}
)
