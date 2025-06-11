from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint


if TYPE_CHECKING:
    from app.schemas.team import ChampionshipParticipation
    from app.schemas.match import Match
    from app.schemas.country import Country

class Championship(SQLModel, table=True):
    __tablename__ = "championships"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, nullable=False) 
    type: Optional[str] = Field(max_length=50, default=None)
    country_id: int = Field(foreign_key="countries.id")
    start_date: Optional[datetime] = Field(default=None)
    end_date: Optional[datetime] = Field(default=None)

    __table_args__ = (UniqueConstraint("name", name="uq_championship_name"),)

    country: Optional["Country"] = Relationship(back_populates="championships")
    participations: List["ChampionshipParticipation"] = Relationship(
        back_populates="championship",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    matches: List["Match"] = Relationship(back_populates="championship")

    def __init__(self, **data):
        super().__init__(**data)
        if len(self.name) > 100:
            raise ValueError("Championship name cannot exceed 100 characters")