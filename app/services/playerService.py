from typing import List, Optional
from datetime import datetime
from app.schemas.player import Player
from app.repositories.playerRepository import PlayerRepository


class PlayerService:
    def __init__(self, repository: PlayerRepository):
        self.repository = repository

    def find_player_by_id(self, player_id: int) -> Player:
        """Find a player by their ID."""
        player = self.repository.get_by_id(player_id)
        if not player:
            raise ValueError("Jogador não encontrado.")
        return player

    def create_player(self, name: str, birth_date: Optional[datetime], country_id: int, position_id: int, team_id: Optional[int] = None) -> Player:
        """Create a new player."""
        self.validate_player_creation(name, birth_date)
        if self.repository.get_by_name(name):
            raise ValueError("Já existe um jogador com esse nome.")
        return self.repository.create(name, birth_date, country_id, position_id, team_id)

    def get_all_players(self) -> List[Player]:
        """Retrieve all players from the database."""
        return self.repository.get_all()

    def update_player(self, player_id: int, name: Optional[str] = None, birth_date: Optional[datetime] = None,
                      country_id: Optional[int] = None, position_id: Optional[int] = None, team_id: Optional[int] = None) -> Player:
        """Update an existing player's information."""
        self.validate_player_update(name, birth_date)
        player = self.repository.update(player_id, name, birth_date, country_id, position_id, team_id)
        if not player:
            raise ValueError("Jogador não encontrado.")
        return player

    def delete_player(self, player_id: int) -> bool:
        """Delete a player by their ID."""
        if not self.repository.get_by_id(player_id):
            raise ValueError("Jogador não encontrado.")
        return self.repository.delete(player_id)

    def validate_player_creation(self, name: str, birth_date: Optional[datetime]):
        """Validate the player creation data."""
        if len(name) < 3:
            raise ValueError("O nome do jogador deve ter pelo menos 3 caracteres.")
        if birth_date and birth_date > datetime.now():
            raise ValueError("A data de nascimento não pode ser no futuro.")

    def validate_player_update(self, name: Optional[str], birth_date: Optional[datetime]):
        """Validate the player update data."""
        if name and len(name) < 3:
            raise ValueError("O nome do jogador deve ter pelo menos 3 caracteres.")
        if birth_date and birth_date > datetime.now():
            raise ValueError("A data de nascimento não pode ser no futuro.")
