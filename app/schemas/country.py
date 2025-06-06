from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class Country(SQLModel, table=True):
    __tablename__ = "countries"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, nullable=False)
    championships: List["Championship"] = Relationship(back_populates="country")
    stadiums: List["Stadium"] = Relationship(back_populates="country")
    players: List["Player"] = Relationship(back_populates="country")
    teams: List["Team"] = Relationship(back_populates="country")