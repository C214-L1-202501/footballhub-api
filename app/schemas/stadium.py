from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import UniqueConstraint

if TYPE_CHECKING:
    from app.schemas.country import Country
    from app.schemas.match import Match

class Stadium(SQLModel, table=True):
    __tablename__ = "stadiums"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    city: Optional[str] = Field(default=None)
    country_id: int = Field(foreign_key="countries.id", nullable=False)
    capacity: Optional[int] = Field(default=None)

    country: Optional["Country"] = Relationship(back_populates="stadiums")
    matches: List["Match"] = Relationship(back_populates="stadium")

    __table_args__ = (UniqueConstraint("name", name="uq_stadium_name"),)

    def __init__(self, **data):
        super().__init__(**data)

        if not self.name:
            raise ValueError("Stadium name is required")
        if not isinstance(self.name, str):
            raise ValueError("Stadium name must be a string")
        if len(self.name) > 100:
            raise ValueError("Stadium name cannot exceed 100 characters")

        if self.city is not None:
            if not isinstance(self.city, str):
                raise ValueError("Stadium city must be a string")
            if len(self.city) > 100:
                raise ValueError("Stadium city cannot exceed 100 characters")

        if self.country_id is None:
            raise ValueError("Country ID is required")