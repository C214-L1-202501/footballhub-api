from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from app.schemas.championship import Championship
    from app.schemas.team import Team
    from app.schemas.stadium import Stadium
    from app.schemas.player import Player

class Country(SQLModel, table=True):
    __tablename__ = "countries"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False) # max_length removido aqui

    teams: List["Team"] = Relationship(back_populates="country")
    championships: List["Championship"] = Relationship(back_populates="country")
    stadiums: List["Stadium"] = Relationship(back_populates="country")
    players: List["Player"] = Relationship(back_populates="country")

    __table_args__ = (UniqueConstraint("name", name="uq_country_name"),)

    def __init__(self, **data):
        super().__init__(**data)

        if not self.name:
            raise ValueError("Country name is required")
        if not isinstance(self.name, str):
            raise ValueError("Country name must be a string")
        if len(self.name) > 100:
            raise ValueError("Country name cannot exceed 100 characters")