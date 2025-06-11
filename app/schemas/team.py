from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from app.schemas.player import Player
    from app.schemas.match import Match, Lineup
    from app.schemas.championship import Championship
    from app.schemas.country import Country

class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False) # max_length removido
    nickname: Optional[str] = Field(default=None) # max_length removido
    city: Optional[str] = Field(default=None) # max_length removido
    country_id: int = Field(foreign_key="countries.id", nullable=False)
    founding_date: Optional[datetime] = Field(default=None)

    country: Optional["Country"] = Relationship(back_populates="teams")
    players: List["Player"] = Relationship(back_populates="team")
    participations: List["ChampionshipParticipation"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    home_matches: List["Match"] = Relationship(
        back_populates="home_team",
        sa_relationship_kwargs={
            "primaryjoin": "Team.id == Match.home_team_id",
            "overlaps": "away_matches"
        }
    )
    away_matches: List["Match"] = Relationship(
        back_populates="away_team",
        sa_relationship_kwargs={
            "primaryjoin": "Team.id == Match.away_team_id",
            "overlaps": "home_matches"
        }
    )
    lineups: List["Lineup"] = Relationship(back_populates="team")

    def __init__(self, **data):
        super().__init__(**data)

        if not self.name:
            raise ValueError("Team name is required")
        if not isinstance(self.name, str):
            raise ValueError("Team name must be a string")
        if len(self.name) > 100:
            raise ValueError("Team name cannot exceed 100 characters")

        if self.nickname is not None:
            if not isinstance(self.nickname, str):
                raise ValueError("Team nickname must be a string")
            if len(self.nickname) > 50:
                raise ValueError("Team nickname cannot exceed 50 characters")

        if self.city is not None:
            if not isinstance(self.city, str):
                raise ValueError("Team city must be a string")
            if len(self.city) > 100:
                raise ValueError("Team city cannot exceed 100 characters")

        if self.country_id is None:
            raise ValueError("Country ID is required")


class ChampionshipParticipation(SQLModel, table=True):
    __tablename__ = "championship_participations"

    id: Optional[int] = Field(default=None, primary_key=True)
    championship_id: int = Field(foreign_key="championships.id", nullable=False)
    team_id: int = Field(foreign_key="teams.id", nullable=False)
    season: Optional[str] = Field(default=None) # max_length removido

    championship: Optional["Championship"] = Relationship(back_populates="participations")
    team: Optional["Team"] = Relationship(back_populates="participations")

    def __init__(self, **data):
        super().__init__(**data)

        if self.championship_id is None:
            raise ValueError("Championship ID is required for Championship Participation")
        if self.team_id is None:
            raise ValueError("Team ID is required for Championship Participation")

        if self.season is not None:
            if not isinstance(self.season, str):
                raise ValueError("Season must be a string")
            if len(self.season) > 20:
                raise ValueError("Season cannot exceed 20 characters")