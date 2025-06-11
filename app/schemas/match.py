from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

from app.schemas.championship import Championship
from app.schemas.player import Player
from app.schemas.stadium import Stadium
from app.schemas.team import Team

class Match(SQLModel, table=True):
    """Match object."""
    __tablename__ = "matches"

    id: Optional[int] = Field(default=None, primary_key=True)
    home_team_id: int = Field(foreign_key="team.id", nullable=False)
    away_team_id: int = Field(foreign_key="team.id", nullable=False)
    championship_id: int = Field(foreign_key="championship.id", nullable=False)
    date: datetime = Field(nullable=False)
    stadium_id: int = Field(foreign_key="stadium.id", nullable=False)
    home_score: Optional[int] = Field(default=None)
    away_score: Optional[int] = Field(default=None)

    home_team: Optional["Team"] = Relationship(sa_relationship_kwargs={"foreign_keys": "Match.home_team_id"})
    away_team: Optional["Team"] = Relationship(sa_relationship_kwargs={"foreign_keys": "Match.away_team_id"})
    championship: Optional["Championship"] = Relationship(back_populates="matches")
    stadium: Optional["Stadium"] = Relationship(back_populates="matches")

    # Constraint: home_team_id != away_team_id (Pydantic validation)
    class Config:
        @staticmethod
        def validate_different_teams(home_team_id: int, away_team_id: int):
            if home_team_id == away_team_id:
                raise ValueError("home_team_id and away_team_id must be different")
            return True

Championship.matches = Relationship(back_populates="championship", sa_relationship_kwargs={"lazy": "selectin"})
Stadium.matches = Relationship(back_populates="stadium", sa_relationship_kwargs={"lazy": "selectin"})

class EventType(SQLModel, table=True):
    """Event Type object."""
    __tablename__ = "event_types"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50, unique=True, nullable=False)

class MatchEvent(SQLModel, table=True):
    """Match Event object."""
    __tablename__ = "match_events"

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="match.id", nullable=False)
    player_id: int = Field(foreign_key="player.id", nullable=False)
    event_type_id: int = Field(foreign_key="event_type.id", nullable=False)
    minute: int = Field(nullable=False)

    match: Optional["Match"] = Relationship(back_populates="events")
    player: Optional["Player"] = Relationship(back_populates="events")
    event_type: Optional["EventType"] = Relationship(back_populates="events")

Match.events = Relationship(back_populates="match", sa_relationship_kwargs={"lazy": "selectin"})
Player.events = Relationship(back_populates="player", sa_relationship_kwargs={"lazy": "selectin"})
EventType.events = Relationship(back_populates="event_type", sa_relationship_kwargs={"lazy": "selectin"})


class Substitution(SQLModel, table=True):
    """Substitution object."""
    __tablename__ = "substitutions"

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="match.id", nullable=False)
    player_out_id: int = Field(foreign_key="player.id", nullable=False)
    player_in_id: int = Field(foreign_key="player.id", nullable=False)
    minute: int = Field(nullable=False)

    match: Optional["Match"] = Relationship(back_populates="substitutions")
    player_out: Optional["Player"] = Relationship(sa_relationship_kwargs={"foreign_keys": "Substitution.player_out_id"})
    player_in: Optional["Player"] = Relationship(sa_relationship_kwargs={"foreign_keys": "Substitution.player_in_id"})

    # Constraint: player_out_id != player_in_id
    class Config:
        @staticmethod
        def validate_different_players(player_out_id: int, player_in_id: int):
            if player_out_id == player_in_id:
                raise ValueError("player_out_id and player_in_id must be different")
            return True

Match.substitutions = Relationship(back_populates="match", sa_relationship_kwargs={"lazy": "selectin"})

class Lineup(SQLModel, table=True):
    """Lineup object."""
    __tablename__ = "lineups"

    id: Optional[int] = Field(default=None, primary_key=True)
    match_id: int = Field(foreign_key="match.id", nullable=False)
    team_id: int = Field(foreign_key="team.id", nullable=False)
    player_id: int = Field(foreign_key="player.id", nullable=False)
    position: Optional[str] = Field(max_length=50, default=None)

    match: Optional["Match"] = Relationship(back_populates="lineups")
    team: Optional["Team"] = Relationship(back_populates="lineups")
    player: Optional["Player"] = Relationship(back_populates="lineups")

    # Constraint: unique(match_id, team_id, player_id)
    __table_args__ = (UniqueConstraint("match_id", "team_id", "player_id"),)

Match.lineups = Relationship(back_populates="match", sa_relationship_kwargs={"lazy": "selectin"})
Team.lineups = Relationship(back_populates="team", sa_relationship_kwargs={"lazy": "selectin"})
Player.lineups = Relationship(back_populates="player", sa_relationship_kwargs={"lazy": "selectin"})