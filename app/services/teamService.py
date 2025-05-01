from typing import List, Optional
from datetime import datetime
from app.schemas.team import Team
from app.repositories.teamRepository import TeamRepository
from app.services.countryService import CountryService


class TeamService:
    def __init__(self, repository: TeamRepository, country_service: CountryService):
        self.repository = repository
        self.country_service = country_service

    def create_team(self, name: str, country_id: int, nickname: Optional[str] = None, 
                   city: Optional[str] = None, founding_date: Optional[datetime] = None) -> Team:
        """Create a new team with validation."""
        # Validate if country exists
        self.country_service.find_country_by_id(country_id)
        
        # Check if team name already exists
        existing_team = self.repository.get_by_name(name)
        if existing_team:
            raise ValueError(f"Team with name already exists.")
        
        return self.repository.create(
            name=name,
            country_id=country_id,
            nickname=nickname,
            city=city,
            founding_date=founding_date
        )

    def get_team_by_id(self, team_id: int) -> Team:
        """Get a team by its ID."""
        team = self.repository.get_by_id(team_id)
        if not team:
            raise ValueError(f"Team with ID {team_id} not found.")
        return team

    def get_team_by_name(self, name: str) -> Team:
        """Get a team by its name."""
        team = self.repository.get_by_name(name)
        if not team:
            raise ValueError(f"Team with name not found.")
        return team

    def get_all_teams(self) -> List[Team]:
        """Get all teams."""
        return self.repository.get_all()

    def update_team(self, team_id: int, name: Optional[str] = None, 
                   country_id: Optional[int] = None, nickname: Optional[str] = None, 
                   city: Optional[str] = None, founding_date: Optional[datetime] = None) -> Team:
        """Update team information."""
        # Get existing team
        team = self.get_team_by_id(team_id)
        
        # Validate country if being updated
        if country_id:
            self.country_service.find_country_by_id(country_id)
        
        # Check if new name already exists (if being changed)
        if name and name != team.name:
            existing_team = self.repository.get_by_name(name)
            if existing_team:
                raise ValueError(f"Team with name already exists.")
        
        updated_team = self.repository.update(
            team_id=team_id,
            name=name,
            country_id=country_id,
            nickname=nickname,
            city=city,
            founding_date=founding_date
        )
        
        if not updated_team:
            raise ValueError("Failed to update team.")
            
        return updated_team

    def delete_team(self, team_id: int) -> bool:
        """Delete a team by its ID."""
        # Verify team exists first
        self.get_team_by_id(team_id)
        return self.repository.delete(team_id)

    def get_teams_by_country(self, country_id: int) -> List[Team]:
        """Get all teams from a specific country."""
        # Validate country exists
        self.country_service.find_country_by_id(country_id)
        
        with self.repository._get_session() as session:
            statement = select(Team).where(Team.country_id == country_id)
            teams = session.exec(statement).all()
            return teams