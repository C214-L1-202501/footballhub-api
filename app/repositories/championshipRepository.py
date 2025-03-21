from typing import List, Optional
from sqlmodel import Session, create_engine, select
import os
from dotenv import load_dotenv

from app.schemas.championship import Championship


class ChampionshipRepository:
    def __init__(self):
        load_dotenv()

        db_uri = os.getenv("DATABASE_URL")
        if not db_uri:
            raise ValueError("DATABASE_URL not found.")

        self.engine = create_engine(db_uri, echo=True)

    def _get_session(self) -> Session:
        return Session(self.engine)

    def create(self, name: str, country_id: Optional[int] = None, type: Optional[str] = None, season: Optional[str] = None) -> Championship:
        """Create a new championship in the database."""
        with self._get_session() as session:
            championship = Championship(name=name, country_id=country_id, type=type, season=season)
            session.add(championship)
            session.commit()
            session.refresh(championship)
            return championship

    def get_by_id(self, championship_id: int) -> Optional[Championship]:
        """Search for a championship by its ID."""
        with self._get_session() as session:
            championship = session.get(Championship, championship_id)
            return championship

    def get_by_name(self, name: str) -> Optional[Championship]:
        """Search for a championship by its name."""
        with self._get_session() as session:
            statement = select(Championship).where(Championship.name == name)
            championship = session.exec(statement).first()
            return championship

    def get_all(self) -> List[Championship]:
        """Returns all championships in the database."""
        with self._get_session() as session:
            statement = select(Championship)
            championships = session.exec(statement).all()
            return championships

    def update(self, championship_id: int, name: Optional[str] = None, country_id: Optional[int] = None, type: Optional[str] = None, season: Optional[str] = None) -> Optional[Championship]:
        """Update the information of an existing championship."""
        with self._get_session() as session:
            championship = session.get(Championship, championship_id)
            if championship:
                if name:
                    championship.name = name
                if country_id:
                    championship.country_id = country_id
                if type:
                    championship.type = type
                if season:
                    championship.season = season
                session.add(championship)
                session.commit()
                session.refresh(championship)
                return championship
            return None

    def delete(self, championship_id: int) -> bool:
        """Delete a championship by its ID. Returns True if successful, False if not found."""
        with self._get_session() as session:
            championship = session.get(Championship, championship_id)
            if championship:
                session.delete(championship)
                session.commit()
                return True
            return False
