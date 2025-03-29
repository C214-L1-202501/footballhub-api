from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

from app.schemas.championship import Championship
from app.schemas.country import Country

if TYPE_CHECKING:
    from app.schemas.player import Player

class Team(SQLModel, table=True):
    """Team object."""
    __tablename__ = "teams"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    nickname: Optional[str] = Field(max_length=50, default=None)
    city: Optional[str] = Field(max_length=100, default=None)
    country_id: int = Field(foreign_key="country.id", nullable=False)
    founding_date: Optional[datetime] = Field(default=None)

    country: Optional["Country"] = Relationship(back_populates="teams")
    players: List["Player"] = Relationship(back_populates="team")

Country.teams = Relationship(back_populates="country", sa_relationship_kwargs={"lazy": "selectin"})

class ChampionshipParticipation(SQLModel, table=True):
    """Championship Participation Object."""
    __tablename__ = "championship_participations"

    id: Optional[int] = Field(default=None, primary_key=True)
    championship_id: int = Field(foreign_key="championship.id", nullable=False)
    team_id: int = Field(foreign_key="team.id", nullable=False)
    season: Optional[str] = Field(max_length=20, default=None)

    championship: Optional["Championship"] = Relationship(back_populates="participations")
    team: Optional["Team"] = Relationship(back_populates="participations")

    # Constraint: unique(championship_id, team_id, season)
    __table_args__ = (UniqueConstraint("championship_id", "team_id", "season"),)

Championship.participations = Relationship(back_populates="championship", sa_relationship_kwargs={"lazy": "selectin"})
Team.participations = Relationship(back_populates="team", sa_relationship_kwargs={"lazy": "selectin"})