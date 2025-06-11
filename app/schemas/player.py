from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from app.schemas.team import Team, Lineup
    from app.schemas.match import Match, Substitution
    from app.schemas.country import Country

class Player(SQLModel, table=True):
    __tablename__ = "players"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False) # max_length removido
    nationality_id: int = Field(foreign_key="countries.id", nullable=False)
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
    birth_date: Optional[datetime] = Field(default=None)
    position: Optional[str] = Field(default=None) # max_length removido

    country: Optional["Country"] = Relationship(back_populates="players")
    team: Optional["Team"] = Relationship(back_populates="players")
    lineups: List["Lineup"] = Relationship(back_populates="player")

    substitutions_out: List["Substitution"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Player.id == Substitution.player_out_id",
            "overlaps": "player_out"
        }
    )
    substitutions_in: List["Substitution"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Player.id == Substitution.player_in_id",
            "overlaps": "player_in"
        }
    )

    __table_args__ = (UniqueConstraint("name", "birth_date", name="uq_player_name_birth_date"),)

    def __init__(self, **data):
        super().__init__(**data)

        if not self.name:
            raise ValueError("Player name is required")
        if not isinstance(self.name, str):
            raise ValueError("Player name must be a string")
        if len(self.name) > 100:
            raise ValueError("Player name cannot exceed 100 characters")

        if self.nationality_id is None:
            raise ValueError("Player nationality ID is required")

        if self.position is not None:
            if not isinstance(self.position, str):
                raise ValueError("Player position must be a string")
            if len(self.position) > 50:
                raise ValueError("Player position cannot exceed 50 characters")