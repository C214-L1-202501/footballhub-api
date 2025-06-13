from typing import List, Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.schemas.player import Player, Position, PlayerOutput
from app.repositories.playerRepository import PlayerRepository


class PlayerService:
    def __init__(self):
        self.repository = PlayerRepository()

    def create_player(
        self,
        name: str,
        birth_date: Optional[datetime],
        country_id: int,
        position_id: int,
        team_id: Optional[int] = None,
    ) -> Player:
        """Cria um novo jogador. Lança ValueError para erros de validação."""
        if not name or len(name.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")

        if any(not isinstance(id, int) or id < 1 for id in [country_id, position_id]):
            raise ValueError("IDs de país e posição devem ser números positivos")

        return self.repository.create(
            name=name.strip(),
            birth_date=birth_date,
            country_id=country_id,
            position_id=position_id,
            team_id=team_id,
        )

    def create_players(self, players: List[Player]) -> List[Player]:
        """Cria múltiplos jogadores. Lança ValueError para erros de validação."""
        created_players = []
        for idx, player in enumerate(players):
            if not player.name or len(player.name.strip()) < 3:
                raise ValueError(f"Nome inválido no jogador índice {idx}")

            if any(
                not isinstance(id, int) or id < 1
                for id in [player.country_id, player.position_id]
            ):
                raise ValueError(f"IDs inválidos no jogador índice {idx}")

            created = self.repository.create(
                name=player.name.strip(),
                birth_date=player.birth_date,
                country_id=player.country_id,
                position_id=player.position_id,
                team_id=player.team_id,
            )
            created_players.append(created)
        return created_players

    def get_player(self, player_id: int) -> Optional[Player]:
        """Obtém um jogador por ID. Retorna None se não encontrado."""
        player = self.repository.get_by_id(player_id)
        position = self.repository.get_position_by_player_id(player_id)
        team = self.repository.get_team_by_player_id(player_id)
        country = self.repository.get_country_by_player_id(player_id)
        player_output = PlayerOutput(
            id=player.id,
            name=player.name,
            birth_date=player.birth_date,
            position=position.name,
            team=team.name,
            country=country.name,
        )

        return player_output if player else None

    def get_all_players(self) -> List[Player]:
        """Lista todos os jogadores."""
        return self.repository.get_all()

    def update_player(
        self,
        player_id: int,
        name: Optional[str] = None,
        birth_date: Optional[datetime] = None,
        country_id: Optional[int] = None,
        position_id: Optional[int] = None,
        team_id: Optional[int] = None,
    ) -> Optional[Player]:
        """Atualiza um jogador. Retorna None se não encontrado."""
        if name and len(name.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")

        if any(
            id is not None and (not isinstance(id, int) or id < 1)
            for id in [country_id, position_id, team_id]
        ):
            raise ValueError("IDs devem ser números positivos")

        return self.repository.update(
            player_id=player_id,
            name=name,
            birth_date=birth_date,
            country_id=country_id,
            position_id=position_id,
            team_id=team_id,
        )

    def delete_player(self, player_id: int) -> bool:
        """Deleta um jogador. Retorna True se deletou, False se não encontrado."""
        return self.repository.delete(player_id)

    def create_positions(self, names: List[str]) -> List[Position]:
        """Cria posições. Lança ValueError para nomes inválidos."""
        if not names:
            raise ValueError("Lista de posições vazia")

        if len(names) > 50:
            raise ValueError("Máximo de 50 posições por requisição")

        for name in names:
            if len(name.strip()) < 3 or len(name.strip()) > 50:
                raise ValueError(f"Nome inválido: '{name}' (3-50 caracteres)")

        return self.repository.create_positions([name.strip() for name in names])
