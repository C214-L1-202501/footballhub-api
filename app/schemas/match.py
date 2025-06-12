from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from app.schemas.team import Team, Lineup
    from app.schemas.player import Player
    from app.schemas.championship import Championship
    from app.schemas.stadium import Stadium
    from app.schemas.match import Substitution

class Match(SQLModel, table=True):
    __tablename__ = "matches"

    id: Optional[int] = Field(default=None, primary_key=True)
    championship_id: int = Field(foreign_key="championships.id", nullable=False)
    match_date: datetime = Field(nullable=False)
    home_team_id: int = Field(foreign_key="teams.id", nullable=False)
    away_team_id: int = Field(foreign_key="teams.id", nullable=False)
    home_team_score: Optional[int] = Field(default=None)
    away_team_score: Optional[int] = Field(default=None)
    status: str = Field(max_length=50, nullable=False, default="scheduled")
    stadium_id: Optional[int] = Field(default=None, foreign_key="stadiums.id")

    championship: Optional["Championship"] = Relationship(back_populates="matches")
    home_team: Optional["Team"] = Relationship(
        back_populates="home_matches",
        sa_relationship_kwargs={
            "primaryjoin": "Team.id == Match.home_team_id",
            "overlaps": "away_team"
        }
    )
    away_team: Optional["Team"] = Relationship(
        back_populates="away_matches",
        sa_relationship_kwargs={
            "primaryjoin": "Team.id == Match.away_team_id",
            "overlaps": "home_team"
        }
    )
    lineups: List["Lineup"] = Relationship(back_populates="match")
    stadium: Optional["Stadium"] = Relationship(back_populates="matches")
    substitutions: List["Substitution"] = Relationship(back_populates="match")

    @classmethod
    def validate_different_teams(cls, home_team_id: int, away_team_id: int) -> bool:
        if home_team_id == away_team_id:
            raise ValueError("home_team_id e away_team_id devem ser diferentes")
        return True

class Substitution(SQLModel, table=True):
    __tablename__ = "substitutions"

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id", nullable=False)
    player_out_id: int = Field(foreign_key="players.id", nullable=False)
    player_in_id: int = Field(foreign_key="players.id", nullable=False)
    minute: int = Field(nullable=False)

    match: Optional[Match] = Relationship(back_populates="substitutions")
    player_out: Optional["Player"] = Relationship(
        sa_relationship_kwargs={"primaryjoin": "Substitution.player_out_id == Player.id"}
    )
    player_in: Optional["Player"] = Relationship(
        sa_relationship_kwargs={"primaryjoin": "Substitution.player_in_id == Player.id"}
    )

    @classmethod
    def validate_different_players(cls, player_out_id: int, player_in_id: int) -> bool:
        if player_out_id == player_in_id:
            raise ValueError("player_out_id e player_in_id devem ser diferentes")
        return True

class Lineup(SQLModel, table=True):
    __tablename__ = "lineups"

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="matches.id", nullable=False)
    team_id: int = Field(foreign_key="teams.id", nullable=False)
    player_id: int = Field(foreign_key="players.id", nullable=False)
    position: str = Field(max_length=50, nullable=False)
    is_starter: bool = Field(default=True)

    match: Optional[Match] = Relationship(back_populates="lineups")
    team: Optional["Team"] = Relationship(back_populates="lineups")
    player: Optional["Player"] = Relationship(back_populates="lineups")