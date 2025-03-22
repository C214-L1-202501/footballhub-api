from typing import List, Optional
from sqlmodel import Session, create_engine, select
import os
from dotenv import load_dotenv

from app.schemas.stadium import Stadium


class StadiumRepository:
    def __init__(self):
        load_dotenv()

        db_uri = os.getenv("DATABASE_URL")
        if not db_uri:
            raise ValueError("DATABASE_URL not found.")

        self.engine = create_engine(db_uri, echo=True)

    def _get_session(self) -> Session:
        return Session(self.engine)

    def create(self, name: str, city: str, country_id: int) -> Stadium:
        """Create a new stadium in the database."""
        with self._get_session() as session:
            stadium = Stadium(name=name, city=city, country_id=country_id)
            session.add(stadium)
            session.commit()
            session.refresh(stadium)
            return stadium

    def get_by_id(self, stadium_id: int) -> Optional[Stadium]:
        """Search for a stadium by its ID."""
        with self._get_session() as session:
            stadium = session.get(Stadium, stadium_id)
            return stadium

    def get_all(self) -> List[Stadium]:
        """Returns all stadiums in the database."""
        with self._get_session() as session:
            statement = select(Stadium)
            stadiums = session.exec(statement).all()
            return stadiums

    def update(self, stadium_id: int, name: Optional[str] = None, city: Optional[str] = None, country_id: Optional[int] = None) -> Optional[Stadium]:
        """Update an existing stadium's information."""
        with self._get_session() as session:
            stadium = session.get(Stadium, stadium_id)
            if stadium:
                if name:
                    stadium.name = name
                if city:
                    stadium.city = city
                if country_id:
                    stadium.country_id = country_id
                session.add(stadium)
                session.commit()
                session.refresh(stadium)
                return stadium
            return None

    def delete(self, stadium_id: int) -> bool:
        """Delete a stadium by its ID. Returns True if successful, False if not found."""
        with self._get_session() as session:
            stadium = session.get(Stadium, stadium_id)
            if stadium:
                session.delete(stadium)
                session.commit()
                return True
            return False
