from app.schemas.entities.Position import Position
from app.repositories.PositionRepository import PositionRepository

class PositionService:
    def __init__(self, repository: PositionRepository):
        self.__repository = repository

    # Adicionar uma posição
    def add_position(self, name: str) -> Position:
        position = Position(name)
        self.__repository.save(position)
        return position