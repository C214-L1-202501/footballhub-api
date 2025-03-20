from typing import List, Optional
from app.schemas.entities.Player import Player

class PlayerRepository:
    def __init__(self):
        self.__players: List[Player] = []

    def save(self, player: Player) -> Player:
        self.__players.append(player)
        return player

    def find_all(self) -> List[Player]:
        return self.__players

    def delete(self, name: str) -> Optional[Player]:
        for player in self.__players:
            if player.name == name:
                self.__players.remove(player)
                return player
        return None
