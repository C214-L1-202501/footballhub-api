from typing import List, Optional
from datetime import datetime

from app.schemas.team import Team
from app.schemas.team import ChampionshipParticipation
from app.schemas.championship import Championship
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
    
    def create_championship_participation(
        self,
        championship_id: int,
        team_id: int,
        season: Optional[str] = None
    ) -> ChampionshipParticipation:
        """
        Cria uma nova participação de time em campeonato.
        Lança ValueError para erros de validação.
        Propaga IntegrityError e SQLAlchemyError para o router tratar.
        """
        # Validação básica
        if not isinstance(championship_id, int) or championship_id < 1:
            raise ValueError("ID do campeonato inválido")
        if not isinstance(team_id, int) or team_id < 1:
            raise ValueError("ID do time inválido")
        if season and len(season) > 20:
            raise ValueError("A temporada deve ter no máximo 20 caracteres")

        return self.repository.create_championshipParticipation(
            championship_id=championship_id,
            team_id=team_id,
            season=season
        )

    def delete_championship_participation(self, participation_id: int) -> bool:
        """
        Remove uma participação de time em campeonato.
        Retorna True se deletou, False se não encontrou.
        Propaga SQLAlchemyError para o router tratar.
        """
        if not isinstance(participation_id, int) or participation_id < 1:
            raise ValueError("ID de participação inválido")
        return self.repository.delete_championshipParticipation(participation_id)
    


    def get_participations_by_team(self, team_id: int):
        with self.repository._get_session() as session:
            from sqlmodel import select
            stmt = (
                select(
                    ChampionshipParticipation.id,
                    ChampionshipParticipation.championship_id,
                    Championship.name.label("championship_name"),
                    ChampionshipParticipation.team_id,
                    ChampionshipParticipation.season
                )
                .join(Championship, Championship.id == ChampionshipParticipation.championship_id)
                .where(ChampionshipParticipation.team_id == team_id)
            )
            results = session.exec(stmt).all()
            participations = [
                {
                    "id": row.id,
                    "championship_id": row.championship_id,
                    "championship_name": row.championship_name,
                    "team_id": row.team_id,
                    "season": row.season,
                }
                for row in results
            ]
            return participations
