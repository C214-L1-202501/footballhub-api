from typing import List, Optional
from app.schemas.entities.Player import Player
from app.repositories.PlayerRepository import PlayerRepository

class PlayersService:
    def __init__(self, repository: PlayerRepository):
        self.__repository = repository

    def add_player(self, name: str, age: int, position: str, country: str, number: int) -> Player:
        player = Player(name, age, position, country, number)
        return self.__repository.save(player)

    def list_players(self) -> List[Player]:
        return self.__repository.find_all()

    def remove_player(self, name: str) -> Optional[Player]:
        return self.__repository.delete(name)
