from typing import Optional
from sqlmodel import SQLModel, Field

class Country(SQLModel, table=True):
    '''Country object.'''
    __tablename__ = "countries"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True, nullable=False)