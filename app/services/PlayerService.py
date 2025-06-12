from typing import List, Optional
from datetime import datetime, date
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.schemas.player import Player


class PlayerService:
    def __init__(self, player_repository=None):
        self.repository = player_repository if player_repository else PlayerRepository()

    def create_player(
        self,
        name: str,
        birth_date: Optional[datetime],
        nationality_id: int,
        position: Optional[str] = None,
        team_id: Optional[int] = None
    ) -> Player:
        
        # Validações de nome e posição adicionadas/ajustadas aqui
        if not name or len(name.strip()) < 3 or len(name.strip()) > 100: # Min e Max
            raise ValueError("Nome deve ter entre 3 e 100 caracteres.")

        if not isinstance(nationality_id, int) or nationality_id < 1:
            raise ValueError("ID da nacionalidade deve ser um número inteiro positivo")
        
        if position is not None: # Validações de tipo e comprimento para position
            if not isinstance(position, str):
                raise ValueError("Posição deve ser uma string ou None.")
            if len(position.strip()) > 50:
                raise ValueError("Posição não pode exceder 50 caracteres.")
        
        if team_id is not None and (not isinstance(team_id, int) or team_id < 1):
            raise ValueError("ID do time deve ser um número inteiro positivo se fornecido")

        try:
            return self.repository.create(
                name=name.strip(),
                birth_date=birth_date,
                nationality_id=nationality_id,
                position=position.strip() if position else None,
                team_id=team_id
            )
        except IntegrityError as e:
            if "uq_player_name_birth_date" in str(e):
                raise ValueError("Já existe um jogador com este nome e data de nascimento.")
            raise ValueError(f"Erro de integridade ao criar jogador: {e}")
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao criar jogador: {e}")

    def create_players(self, players_data: List[dict]) -> List[Player]:
        created_players = []
        for idx, player_data in enumerate(players_data):
            name = player_data.get("name")
            birth_date = player_data.get("birth_date")
            nationality_id = player_data.get("nationality_id")
            position = player_data.get("position")
            team_id = player_data.get("team_id")

            # Validações básicas antes de tentar criar a instância do Player
            if not name or len(name.strip()) < 3 or len(name.strip()) > 100: # Min e Max
                raise ValueError(f"Nome inválido no jogador índice {idx}: '{name}' (3-100 caracteres)")
            if not isinstance(nationality_id, int) or nationality_id < 1:
                raise ValueError(f"ID da nacionalidade inválido no jogador índice {idx}: '{nationality_id}'")
            if position is not None:
                if not isinstance(position, str) :
                    raise ValueError(f"Posição inválida no jogador índice {idx}: '{position}' (deve ser string ou None)")
                if len(position.strip()) > 50:
                    raise ValueError(f"Posição inválida no jogador índice {idx}: '{position}' (máx 50 caracteres)")
            
            if team_id is not None and (not isinstance(team_id, int) or team_id < 1):
                raise ValueError(f"ID do time inválido no jogador índice {idx}: '{team_id}'")
            
            try:
                created = self.repository.create(
                    name=name.strip(),
                    birth_date=birth_date,
                    nationality_id=nationality_id,
                    position=position.strip() if position else None,
                    team_id=team_id
                )
                created_players.append(created)
            except IntegrityError as e:
                if "uq_player_name_birth_date" in str(e):
                    raise ValueError(f"Já existe um jogador com este nome e data de nascimento no índice {idx}.")
                raise ValueError(f"Erro de integridade ao criar jogador no índice {idx}: {e}")
            except SQLAlchemyError as e:
                raise Exception(f"Erro no banco de dados ao criar jogador no índice {idx}: {e}")

        return created_players


    def get_player(self, player_id: int) -> Player:
        player = self.repository.get_by_id(player_id)
        if not player:
            raise ValueError("Jogador não encontrado.")
        return player

    def get_all_players(self) -> List[Player]:
        return self.repository.get_all()

    def update_player(
        self,
        player_id: int,
        name: Optional[str] = None,
        birth_date: Optional[datetime] = None,
        nationality_id: Optional[int] = None,
        position: Optional[str] = None,
        team_id: Optional[int] = None
    ) -> Player:
        
        player = self.repository.get_by_id(player_id)
        if not player:
            raise ValueError("Jogador não encontrado.")

        if name is not None:
            if not isinstance(name, str) or len(name.strip()) < 3 or len(name.strip()) > 100:
                raise ValueError("Nome deve ser uma string com 3 a 100 caracteres")

        if nationality_id is not None:
            if not isinstance(nationality_id, int) or nationality_id < 1:
                raise ValueError("ID da nacionalidade deve ser um número inteiro positivo")
        
        if position is not None:
            if not isinstance(position, str) :
                raise ValueError("Posição deve ser uma string ou None.")
            if len(position.strip()) > 50:
                raise ValueError("Posição não pode exceder 50 caracteres.")
        
        if team_id is not None:
            if not isinstance(team_id, int) or team_id < 1:
                raise ValueError("ID do time deve ser um número inteiro positivo")
            
        try:
            updated_player = self.repository.update(
                player_id=player_id,
                name=name.strip() if name is not None else None,
                birth_date=birth_date,
                nationality_id=nationality_id,
                position=position.strip() if position is not None else None,
                team_id=team_id
            )
            if not updated_player:
                raise Exception("Erro desconhecido ao atualizar jogador.")
            return updated_player
        except IntegrityError as e:
            if "uq_player_name_birth_date" in str(e):
                raise ValueError("Já existe um jogador com este nome e data de nascimento.")
            raise ValueError(f"Erro de integridade ao atualizar jogador: {e}")
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao atualizar jogador: {e}")

    def delete_player(self, player_id: int) -> bool: # MÉTODO delete_player ESTÁ AQUI
        player = self.repository.get_by_id(player_id)
        if not player:
            raise ValueError("Jogador não encontrado.")
        return self.repository.delete(player_id)