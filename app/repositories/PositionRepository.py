from typing import List
from app.schemas.entities.Position import Position

class PositionRepository:
    def __init__(self):
        self.__positions: List[Position] = []

    def save(self, position: Position) -> Position:
        self.__positions.append(position)