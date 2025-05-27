from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.schemas.team import Team
from app.schemas.player import Player
from app.repositories.teamRepository import TeamRepository


class TeamService:
    def __init__(self):
        self.repository = TeamRepository()

    def create_team(
        self,
        name: str,
        country_id: int,
        nickname: Optional[str] = None,
        city: Optional[str] = None,
        founding_date: Optional[datetime] = None
    ) -> Team:
        """
        Cria um novo time com validação básica.
        Lança ValueError para erros de validação.
        Propaga IntegrityError e SQLAlchemyError para o router tratar.
        """
        # Validação básica
        if not name or len(name.strip()) < 3:
            raise ValueError("Nome do time deve ter pelo menos 3 caracteres")

        if not isinstance(country_id, int) or country_id < 1:
            raise ValueError("ID do país inválido")

        # Criação do time
        return self.repository.create(
            name=name.strip(),
            country_id=country_id,
            nickname=nickname.strip() if nickname else None,
            city=city.strip() if city else None,
            founding_date=founding_date
        )

    def get_team(self, team_id: int) -> Optional[Team]:
        """
        Obtém um time por ID.
        Retorna None se não encontrado.
        Propaga SQLAlchemyError para o router tratar.
        """
        return self.repository.get_by_id(team_id)

    def search_teams(self, name: str) -> Optional[Team]:
        """
        Busca times por nome.
        Propaga SQLAlchemyError para o router tratar.
        """
        return self.repository.get_by_name(name)

    def get_all_teams(self) -> List[Team]:
        """
        Lista todos os times.
        Propaga SQLAlchemyError para o router tratar.
        """
        return self.repository.get_all()

    def update_team(
        self,
        team_id: int,
        name: Optional[str] = None,
        country_id: Optional[int] = None,
        nickname: Optional[str] = None,
        city: Optional[str] = None,
        founding_date: Optional[datetime] = None
    ) -> Optional[Team]:
        """
        Atualiza um time existente.
        Lança ValueError para erros de validação.
        Retorna None se o time não existe.
        Propaga IntegrityError e SQLAlchemyError para o router tratar.
        """
        if name and len(name.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")

        if country_id is not None and country_id < 1:
            raise ValueError("ID de país inválido")

        updated_team = self.repository.update(
            team_id=team_id,
            name=name,
            country_id=country_id,
            nickname=nickname,
            city=city,
            founding_date=founding_date
        )
        return updated_team

    def delete_team(self, team_id: int) -> bool:
        """
        Remove um time permanentemente.
        Retorna True se deletou, False se não encontrou.
        Propaga SQLAlchemyError para o router tratar.
        """
        return self.repository.delete(team_id)

    def get_players_by_team(self, team_id: int) -> List[Player]:
        """
        Retorna todos os jogadores de um time.
        Propaga SQLAlchemyError para o router tratar.
        """
        return self.repository.get_players(team_id)
