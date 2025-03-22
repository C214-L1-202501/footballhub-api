from typing import List, Optional
from datetime import datetime
from app.schemas.team import Team
from app.repositories.teamRepository import TeamRepository


class TeamService:
    def __init__(self, repository: TeamRepository):
        self.repository = repository

    def find_team_by_id(self, team_id: int) -> Team:
        """Find a team by its ID."""
        team = self.repository.get_by_id(team_id)
        if not team:
            raise ValueError("Time não encontrado.")
        return team

    def create_team(self, name: str, country_id: int, nickname: Optional[str] = None, city: Optional[str] = None, founding_date: Optional[datetime] = None) -> Team:
        """Create a new team."""
        self.validate_team_creation(name, founding_date)
        if self.repository.get_by_name(name):
            raise ValueError("Já existe um time com esse nome.")
        return self.repository.create(name, country_id, nickname, city, founding_date)

    def get_all_teams(self) -> List[Team]:
        """Retrieve all teams from the database."""
        return self.repository.get_all()

    def update_team(self, team_id: int, name: Optional[str] = None, country_id: Optional[int] = None, 
                    nickname: Optional[str] = None, city: Optional[str] = None, founding_date: Optional[datetime] = None) -> Team:
        """Update an existing team's information."""
        self.validate_team_update(name, founding_date)
        team = self.repository.update(team_id, name, country_id, nickname, city, founding_date)
        if not team:
            raise ValueError("Time não encontrado.")
        return team

    def delete_team(self, team_id: int) -> bool:
        """Delete a team by its ID."""
        if not self.repository.get_by_id(team_id):
            raise ValueError("Time não encontrado.")
        return self.repository.delete(team_id)

    def validate_team_creation(self, name: str, founding_date: Optional[datetime]):
        """Validate the team creation data."""
        if len(name) < 3:
            raise ValueError("O nome do time deve ter pelo menos 3 caracteres.")
        if founding_date and founding_date > datetime.now():
            raise ValueError("A data de fundação não pode ser no futuro.")

    def validate_team_update(self, name: Optional[str], founding_date: Optional[datetime]):
        """Validate the team update data."""
        if name and len(name) < 3:
            raise ValueError("O nome do time deve ter pelo menos 3 caracteres.")
        if founding_date and founding_date > datetime.now():
            raise ValueError("A data de fundação não pode ser no futuro.")
