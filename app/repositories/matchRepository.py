from typing import List, Optional
from sqlmodel import Session, create_engine, select
import os
from dotenv import load_dotenv
from datetime import datetime

from app.schemas.match import Match


class MatchRepository:
    def __init__(self):
        load_dotenv()

        db_uri = os.getenv("DATABASE_URL")
        if not db_uri:
            raise ValueError("DATABASE_URL not found.")

        self.engine = create_engine(db_uri, echo=True)

    def _get_session(self) -> Session:
        return Session(self.engine)

    def create(self, home_team_id: int, away_team_id: int, championship_id: int, date: datetime, stadium_id: int, home_score: Optional[int] = None, away_score: Optional[int] = None) -> Match:
        """Create a new match in the database."""
        with self._get_session() as session:
            match = Match(
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                championship_id=championship_id,
                date=date,
                stadium_id=stadium_id,
                home_score=home_score,
                away_score=away_score
            )
            session.add(match)
            session.commit()
            session.refresh(match)
            return match

    def get_by_id(self, match_id: int) -> Optional[Match]:
        """Search for a match by its ID."""
        with self._get_session() as session:
            match = session.get(Match, match_id)
            return match

    def get_by_teams(self, home_team_id: int, away_team_id: int) -> Optional[Match]:
        """Search for a match by home and away team IDs."""
        with self._get_session() as session:
            statement = select(Match).where(Match.home_team_id == home_team_id, Match.away_team_id == away_team_id)
            match = session.exec(statement).first()
            return match

    def get_all(self) -> List[Match]:
        """Returns all matches in the database."""
        with self._get_session() as session:
            statement = select(Match)
            matches = session.exec(statement).all()
            return matches

    def update(self, match_id: int, home_team_id: Optional[int] = None, away_team_id: Optional[int] = None, championship_id: Optional[int] = None, date: Optional[datetime] = None, stadium_id: Optional[int] = None, home_score: Optional[int] = None, away_score: Optional[int] = None) -> Optional[Match]:
        """Update an existing match's information."""
        with self._get_session() as session:
            match = session.get(Match, match_id)
            if match:
                if home_team_id:
                    match.home_team_id = home_team_id
                if away_team_id:
                    match.away_team_id = away_team_id
                if championship_id:
                    match.championship_id = championship_id
                if date:
                    match.date = date
                if stadium_id:
                    match.stadium_id = stadium_id
                if home_score is not None:
                    match.home_score = home_score
                if away_score is not None:
                    match.away_score = away_score
                session.add(match)
                session.commit()
                session.refresh(match)
                return match
            return None

    def delete(self, match_id: int) -> bool:
        """Delete a match by its ID. Returns True if successful, False if not found."""
        with self._get_session() as session:
            match = session.get(Match, match_id)
            if match:
                session.delete(match)
                session.commit()
                return True
            return False
