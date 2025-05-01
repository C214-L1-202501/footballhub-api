from typing import List, Optional
from datetime import datetime
from app.schemas.player import Player
from app.repositories.playerRepository import PlayerRepository


class PlayerService:
    def __init__(self, repository: PlayerRepository):
        self.repository = repository

    def create_player(self, name: str, birth_date: Optional[datetime], country_id: int, 
                      position_id: int, team_id: Optional[int] = None) -> Player:
        """Create a new player after validating input."""
        if not name:
            raise ValueError("Player name is required.")
        if country_id <= 0 or position_id <= 0:
            raise ValueError("Invalid country or position ID.")
        
        return self.repository.create(
            name=name,
            birth_date=birth_date,
            country_id=country_id,
            position_id=position_id,
            team_id=team_id
        )

    def get_player_by_id(self, player_id: int) -> Player:
        """Retrieve a player by ID with validation."""
        player = self.repository.get_by_id(player_id)
        if not player:
            raise ValueError(f"Player with ID not found.")
        return player

    def get_player_by_name(self, name: str) -> Player:
        """Retrieve a player by name."""
        player = self.repository.get_by_name(name)
        if not player:
            raise ValueError(f"Player with name not found.")
        return player

    def get_all_players(self) -> List[Player]:
        """List all players."""
        return self.repository.get_all()

    def update_player(self, player_id: int, name: Optional[str] = None, 
                      birth_date: Optional[datetime] = None, 
                      country_id: Optional[int] = None, 
                      position_id: Optional[int] = None, 
                      team_id: Optional[int] = None) -> Player:
        """Update a player's information with validation."""
        existing = self.repository.get_by_id(player_id)
        if not existing:
            raise ValueError(f"Player with ID not found.")

        updated = self.repository.update(
            player_id=player_id,
            name=name,
            birth_date=birth_date,
            country_id=country_id,
            position_id=position_id,
            team_id=team_id
        )
        if not updated:
            raise ValueError("Failed to update player.")
        return updated

    def delete_player(self, player_id: int) -> bool:
        """Delete a player by ID after validating existence."""
        existing = self.repository.get_by_id(player_id)
        if not existing:
            raise ValueError(f"Player with ID not found.")

        return self.repository.delete(player_id)
