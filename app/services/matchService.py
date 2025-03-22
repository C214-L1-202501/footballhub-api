from typing import List, Optional
from datetime import datetime
from app.schemas.match import Match
from app.repositories.matchRepository import MatchRepository

class MatchService:
    def __init__(self, repository: MatchRepository):
        self.repository = repository

    def find_match_by_id(self, match_id: int) -> Match:
        """Find a match by its ID."""
        match = self.repository.get_by_id(match_id)
        if not match:
            raise Exception("Partida não encontrada.")
        return match

    def create_match(self, home_team_id: int, away_team_id: int, championship_id: int, date: datetime, stadium_id: int, home_score: Optional[int] = None, away_score: Optional[int] = None) -> Match:
        """Create a new match."""
        self.validate_match_creation(home_team_id, away_team_id, championship_id, date, stadium_id)
        return self.repository.create(home_team_id, away_team_id, championship_id, date, stadium_id, home_score, away_score)

    def get_all_matches(self) -> List[Match]:
        """Retrieve all matches from the database."""
        return self.repository.get_all()

    def update_match(self, match_id: int, home_team_id: Optional[int] = None, away_team_id: Optional[int] = None, championship_id: Optional[int] = None, date: Optional[datetime] = None, stadium_id: Optional[int] = None, home_score: Optional[int] = None, away_score: Optional[int] = None) -> Match:
        """Update an existing match's information."""
        self.validate_match_update(home_team_id, away_team_id, championship_id, date, stadium_id, home_score, away_score)
        match = self.repository.get_by_id(match_id)
        if not match:
            raise Exception("Partida não encontrada.")
        return self.repository.update(match_id, home_team_id, away_team_id, championship_id, date, stadium_id, home_score, away_score)

    def delete_match(self, match_id: int) -> bool:
        """Delete a match by its ID."""
        match = self.repository.get_by_id(match_id)
        if not match:
            raise Exception("Partida não encontrada.")
        return self.repository.delete(match_id)

    def validate_match_creation(self, home_team_id: int, away_team_id: int, championship_id: int, date: datetime, stadium_id: int):
        """Validate the match creation data."""
        if home_team_id == away_team_id:
            raise Exception("O time mandante e o visitante não podem ser o mesmo.")
        if date < datetime.now():
            raise Exception("A data da partida não pode estar no passado.")

    def validate_match_update(self, home_team_id: Optional[int], away_team_id: Optional[int], championship_id: Optional[int], date: Optional[datetime], stadium_id: Optional[int], home_score: Optional[int], away_score: Optional[int]):
        """Validate the match update data."""
        if home_team_id and away_team_id and home_team_id == away_team_id:
            raise Exception("O time mandante e o visitante não podem ser o mesmo.")
        if date and date < datetime.now():
            raise Exception("A data da partida não pode estar no passado.")
