from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship




class Championship(SQLModel, table=True):
    """Championship object."""
    __tablename__ = "championships"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    country_id: Optional[int] = Field(default=None, foreign_key="countries.id")
    type: Optional[str] = Field(max_length=50, default=None)
    season: Optional[str] = Field(max_length=20, default=None)

    country: Optional["Country"] = Relationship(back_populates="championships")
    participations: List["ChampionshipParticipation"] = Relationship(
        back_populates="championship",
        sa_relationship_kwargs={"lazy": "selectin"})