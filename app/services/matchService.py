from typing import List, Optional
from datetime import datetime
from app.schemas.match import Match
from app.repositories.matchRepository import MatchRepository
from app.services.teamService import TeamService
from app.services.championshipService import ChampionshipService
from app.services.stadiumService import StadiumService


class MatchService:
    def __init__(self, repository: MatchRepository, 
                 team_service: TeamService,
                 championship_service: ChampionshipService,
                 stadium_service: StadiumService):
        self.repository = repository
        self.team_service = team_service
        self.championship_service = championship_service
        self.stadium_service = stadium_service

    def create_match(self, home_team_id: int, away_team_id: int, 
                    championship_id: int, date: datetime, stadium_id: int,
                    home_score: Optional[int] = None, 
                    away_score: Optional[int] = None) -> Match:
        # Validate teams exist
        home_team = self.team_service.get_team_by_id(home_team_id)
        away_team = self.team_service.get_team_by_id(away_team_id)
        
        # Teams can't be the same
        if home_team_id == away_team_id:
            raise ValueError("Home team and away team cannot be the same.")
        
        # Validate championship exists
        self.championship_service.get_championship_by_id(championship_id)
        
        # Validate stadium exists
        self.stadium_service.get_stadium_by_id(stadium_id)
        
        # Validate date is in the future for new matches
        if date < datetime.now():
            raise ValueError("Match date cannot be in the past.")
        
        # Check if teams already have a match scheduled at this time
        existing_match = self._check_team_availability(home_team_id, away_team_id, date)
        if existing_match:
            raise ValueError(f"One or both teams already have a match scheduled at this time (Match ID: {existing_match.id})")
        
        return self.repository.create(
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            championship_id=championship_id,
            date=date,
            stadium_id=stadium_id,
            home_score=home_score,
            away_score=away_score
        )

    def get_match_by_id(self, match_id: int) -> Match:
        """Get a match by its ID."""
        match = self.repository.get_by_id(match_id)
        if not match:
            raise ValueError(f"Match with ID {match_id} not found.")
        return match

    def get_matches_by_team(self, team_id: int) -> List[Match]:
        """Get all matches for a specific team (either home or away)."""
        self.team_service.get_team_by_id(team_id)  # Validate team exists
        
        with self.repository._get_session() as session:
            statement = select(Match).where(
                (Match.home_team_id == team_id) | 
                (Match.away_team_id == team_id)
            )
            matches = session.exec(statement).all()
            return matches

    def get_matches_by_championship(self, championship_id: int) -> List[Match]:
        """Get all matches for a specific championship."""
        self.championship_service.get_championship_by_id(championship_id)  # Validate championship exists
        
        with self.repository._get_session() as session:
            statement = select(Match).where(
                Match.championship_id == championship_id
            )
            matches = session.exec(statement).all()
            return matches

    def get_matches_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Match]:
        """Get all matches within a date range."""
        if start_date > end_date:
            raise ValueError("Start date cannot be after end date.")
            
        with self.repository._get_session() as session:
            statement = select(Match).where(
                Match.date >= start_date,
                Match.date <= end_date
            ).order_by(Match.date)
            matches = session.exec(statement).all()
            return matches

    def update_match(self, match_id: int, 
                    home_team_id: Optional[int] = None, 
                    away_team_id: Optional[int] = None, 
                    championship_id: Optional[int] = None, 
                    date: Optional[datetime] = None, 
                    stadium_id: Optional[int] = None, 
                    home_score: Optional[int] = None, 
                    away_score: Optional[int] = None) -> Match:
        """Update match information with validation."""
        match = self.get_match_by_id(match_id)
        
        # Validate teams if being updated
        if home_team_id is not None:
            self.team_service.get_team_by_id(home_team_id)
        if away_team_id is not None:
            self.team_service.get_team_by_id(away_team_id)
        
        # Teams can't be the same
        if (home_team_id is not None and away_team_id is not None and 
            home_team_id == away_team_id):
            raise ValueError("Home team and away team cannot be the same.")
        
        # Validate championship if being updated
        if championship_id is not None:
            self.championship_service.get_championship_by_id(championship_id)
        
        # Validate stadium if being updated
        if stadium_id is not None:
            self.stadium_service.get_stadium_by_id(stadium_id)
        
        # Validate date if being updated
        if date is not None:
            if date < datetime.now():
                raise ValueError("Match date cannot be in the past.")
            
            # Check team availability for new date
            ht_id = home_team_id if home_team_id is not None else match.home_team_id
            at_id = away_team_id if away_team_id is not None else match.away_team_id
            
            existing_match = self._check_team_availability(ht_id, at_id, date, exclude_match_id=match_id)
            if existing_match:
                raise ValueError(f"One or both teams already have a match scheduled at this time (Match ID: {existing_match.id})")
        
        updated_match = self.repository.update(
            match_id=match_id,
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            championship_id=championship_id,
            date=date,
            stadium_id=stadium_id,
            home_score=home_score,
            away_score=away_score
        )
        
        if not updated_match:
            raise ValueError("Failed to update match.")
            
        return updated_match

    def delete_match(self, match_id: int) -> bool:
        """Delete a match by its ID."""
        # Verify match exists first
        self.get_match_by_id(match_id)
        return self.repository.delete(match_id)

    def _check_team_availability(self, home_team_id: int, away_team_id: int, 
                               date: datetime, exclude_match_id: Optional[int] = None) -> Optional[Match]:
     
        with self.repository._get_session() as session:
            # Define a time window to check (e.g., ±3 hours from match time)
            time_window_start = date - timedelta(hours=3)
            time_window_end = date + timedelta(hours=3)
            
            query = select(Match).where(
                (
                    (Match.home_team_id == home_team_id) |
                    (Match.away_team_id == home_team_id) |
                    (Match.home_team_id == away_team_id) |
                    (Match.away_team_id == away_team_id)
                ),
                (Match.date >= time_window_start),
                (Match.date <= time_window_end)
            )
            
            if exclude_match_id:
                query = query.where(Match.id != exclude_match_id)
                
            conflicting_match = session.exec(query).first()
            return conflicting_match

    def get_head_to_head(self, team1_id: int, team2_id: int) -> List[Match]:
        """Get all historical matches between two teams."""
        self.team_service.get_team_by_id(team1_id)
        self.team_service.get_team_by_id(team2_id)
        
        with self.repository._get_session() as session:
            statement = select(Match).where(
                (
                    (Match.home_team_id == team1_id) & 
                    (Match.away_team_id == team2_id)
                ) | (
                    (Match.home_team_id == team2_id) & 
                    (Match.away_team_id == team1_id)
                )
            ).order_by(Match.date.desc())
            matches = session.exec(statement).all()
            return matches