from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from app.schemas.country import Country

if TYPE_CHECKING:
    from app.schemas.team import Team

class Player(SQLModel, table=True):
    """Player object."""
    __tablename__ = "players"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    birth_date: Optional[datetime] = Field(default=None)
    country_id: int = Field(foreign_key="country.id", nullable=False)
    position_id: int = Field(foreign_key="position.id", nullable=False)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    country: Optional["Country"] = Relationship(back_populates="players")
    position: Optional["Position"] = Relationship(back_populates="players")
    team: Optional["Team"] = Relationship(back_populates="players")

class Position(SQLModel, table=True):
    """Player position object."""
    __tablename__ = "positions"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, nullable=False)