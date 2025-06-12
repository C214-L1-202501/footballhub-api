from typing import List, Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.schemas.team import Team
from app.schemas.team import ChampionshipParticipation
from app.schemas.player import Player
from app.repositories.teamRepository import TeamRepository


class TeamService:
    def __init__(self, team_repository: TeamRepository = None):
        self.repository = team_repository if team_repository else TeamRepository()

    def create_team(
        self,
        name: str,
        country_id: int,
        nickname: Optional[str] = None,
        city: Optional[str] = None,
        founding_date: Optional[datetime] = None
    ) -> Team:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nome do time é obrigatório.")
        normalized_name = name.strip()
        if len(normalized_name) < 3 or len(normalized_name) > 100:
            raise ValueError("Nome do time deve ter entre 3 e 100 caracteres.")

        if not isinstance(country_id, int) or country_id < 1:
            raise ValueError("ID do país deve ser um número inteiro positivo.")

        normalized_nickname = nickname.strip() if nickname else None
        if normalized_nickname and (len(normalized_nickname) < 2 or len(normalized_nickname) > 50):
            raise ValueError("Apelido do time deve ter entre 2 e 50 caracteres (se fornecido).")

        normalized_city = city.strip() if city else None
        if normalized_city and (len(normalized_city) < 2 or len(normalized_city) > 100):
            raise ValueError("Cidade do time deve ter entre 2 e 100 caracteres (se fornecida).")

        if founding_date is not None and not isinstance(founding_date, datetime):
            raise ValueError("Data de fundação inválida. Deve ser um objeto datetime.")
        if founding_date and founding_date > datetime.now():
            raise ValueError("Data de fundação não pode ser no futuro.")

        try:
            return self.repository.create(
                name=normalized_name,
                country_id=country_id,
                nickname=normalized_nickname,
                city=normalized_city,
                founding_date=founding_date
            )
        except IntegrityError as e:
            if "uq_team_name" in str(e) or "duplicate key value violates unique constraint" in str(e):
                raise ValueError(f"Já existe um time com o nome '{normalized_name}'.")
            raise ValueError(f"Erro de integridade ao criar time: {e}")
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao criar time: {e}")
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado ao criar time: {e}")

    def get_team(self, team_id: int) -> Team:
        if not isinstance(team_id, int) or team_id < 1:
            raise ValueError("ID do time deve ser um número inteiro positivo.")

        try:
            team = self.repository.get_by_id(team_id)
            if not team:
                raise ValueError(f"Time com ID {team_id} não encontrado.")
            return team
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao buscar time por ID: {e}")

    def search_teams(self, name: str) -> List[Team]:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nome para busca do time deve ser uma string não vazia.")
        normalized_name = name.strip()
        
        try:
            team = self.repository.get_by_name(normalized_name)
            if not team:
                raise ValueError(f"Time com nome '{normalized_name}' não encontrado.")
            return [team]
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao buscar time por nome: {e}")

    def get_all_teams(self) -> List[Team]:
        try:
            return self.repository.get_all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao recuperar todos os times: {e}")
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado ao recuperar todos os times: {e}")

    def update_team(
        self,
        team_id: int,
        name: Optional[str] = None,
        country_id: Optional[int] = None,
        nickname: Optional[str] = None,
        city: Optional[str] = None,
        founding_date: Optional[datetime] = None
    ) -> Team:
        if not isinstance(team_id, int) or team_id < 1:
            raise ValueError("ID do time deve ser um número inteiro positivo.")

        existing_team = self.repository.get_by_id(team_id)
        if not existing_team:
            raise ValueError(f"Time com ID {team_id} não encontrado para atualização.")

        update_data = {}
        if name is not None:
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Nome do time não pode ser vazio ou inválido.")
            normalized_name = name.strip()
            if len(normalized_name) < 3 or len(normalized_name) > 100:
                raise ValueError("Nome do time deve ter entre 3 e 100 caracteres.")
            update_data['name'] = normalized_name

        if country_id is not None:
            if not isinstance(country_id, int) or country_id < 1:
                raise ValueError("ID do país deve ser um número inteiro positivo.")
            update_data['country_id'] = country_id

        if nickname is not None:
            normalized_nickname = nickname.strip() if nickname else None
            if normalized_nickname and (len(normalized_nickname) < 2 or len(normalized_nickname) > 50):
                raise ValueError("Apelido do time deve ter entre 2 e 50 caracteres (se fornecido).")
            update_data['nickname'] = normalized_nickname

        if city is not None:
            normalized_city = city.strip() if city else None
            if normalized_city and (len(normalized_city) < 2 or len(normalized_city) > 100):
                raise ValueError("Cidade do time deve ter entre 2 e 100 caracteres (se fornecida).")
            update_data['city'] = normalized_city

        if founding_date is not None:
            if not isinstance(founding_date, datetime):
                raise ValueError("Data de fundação inválida. Deve ser um objeto datetime.")
            if founding_date > datetime.now():
                raise ValueError("Data de fundação não pode ser no futuro.")
            update_data['founding_date'] = founding_date
        
        if not update_data:
            return existing_team

        try:
            updated_team = self.repository.update(team_id, **update_data)
            if not updated_team:
                raise Exception(f"Falha ao atualizar o time com ID {team_id}.")
            return updated_team
        except IntegrityError as e:
            if "uq_team_name" in str(e) or "duplicate key value violates unique constraint" in str(e):
                raise ValueError(f"Já existe um time com o nome '{update_data.get('name')}' após a atualização.")
            raise ValueError(f"Erro de integridade ao atualizar time: {e}")
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao atualizar time: {e}")
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado ao atualizar time: {e}")

    def delete_team(self, team_id: int) -> bool:
        if not isinstance(team_id, int) or team_id < 1:
            raise ValueError("ID do time deve ser um número inteiro positivo.")

        try:
            team = self.repository.get_by_id(team_id)
            if not team:
                raise ValueError(f"Time com ID {team_id} não encontrado para exclusão.")
            
            return self.repository.delete(team_id)
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao excluir time: {e}")

    def get_players_by_team(self, team_id: int) -> List[Player]:
        if not isinstance(team_id, int) or team_id < 1:
            raise ValueError("ID do time deve ser um número inteiro positivo.")
        
        try:
            team = self.repository.get_by_id(team_id)
            if not team:
                raise ValueError(f"Time com ID {team_id} não encontrado para listar jogadores.")
            
            return self.repository.get_players_for_team(team_id)
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao recuperar jogadores do time: {e}")
    
    def create_championship_participation(
        self,
        championship_id: int,
        team_id: int,
        season: Optional[str] = None
    ) -> ChampionshipParticipation:
        if not isinstance(championship_id, int) or championship_id < 1:
            raise ValueError("ID do campeonato deve ser um número inteiro positivo.")
        if not isinstance(team_id, int) or team_id < 1:
            raise ValueError("ID do time deve ser um número inteiro positivo.")
        
        normalized_season = season.strip() if season else None
        if normalized_season and len(normalized_season) > 20:
            raise ValueError("A temporada deve ter no máximo 20 caracteres (se fornecida).")

        try:
            return self.repository.create_championship_participation(
                championship_id=championship_id,
                team_id=team_id,
                season=normalized_season
            )
        except IntegrityError as e:
            if "uq_championship_participation" in str(e) or "duplicate key value violates unique constraint" in str(e):
                raise ValueError(f"Esta participação em campeonato já existe para o time {team_id} e campeonato {championship_id} na temporada {normalized_season}.")
            raise ValueError(f"Erro de integridade ao criar participação em campeonato: {e}")
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao criar participação em campeonato: {e}")
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado ao criar participação em campeonato: {e}")

    def delete_championship_participation(self, participation_id: int) -> bool:
        if not isinstance(participation_id, int) or participation_id < 1:
            raise ValueError("ID de participação deve ser um número inteiro positivo.")
        
        try:
            participation = self.repository.get_championship_participation_by_id(participation_id)
            if not participation:
                raise ValueError(f"Participação em campeonato com ID {participation_id} não encontrada para exclusão.")

            return self.repository.delete_championship_participation(participation_id)
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao excluir participação em campeonato: {e}")
    
    def get_participations_by_team(self, team_id: int):
        if not isinstance(team_id, int) or team_id < 1:
            raise ValueError("ID do time deve ser um número inteiro positivo.")
        
        try:
            team = self.repository.get_by_id(team_id)
            if not team:
                raise ValueError(f"Time com ID {team_id} não encontrado para listar participações em campeonatos.")
            
            return self.repository.get_team_championship_participations(team_id)
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao recuperar participações em campeonatos do time: {e}")