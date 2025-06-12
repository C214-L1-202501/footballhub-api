from typing import List, Optional
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.schemas.stadium import Stadium
from app.repositories.stadiumRepository import StadiumRepository


class StadiumService:
    def __init__(self, stadium_repository: StadiumRepository = None):
        self.repository = stadium_repository if stadium_repository else StadiumRepository()

    def find_stadium_by_id(self, stadium_id: int) -> Stadium:
        """
        Encontra um estádio pelo seu ID.
        Levanta ValueError se o ID for inválido ou o estádio não for encontrado.
        """
        if not isinstance(stadium_id, int) or stadium_id < 1:
            raise ValueError("ID do estádio deve ser um número inteiro positivo.")
        
        try:
            stadium = self.repository.get_by_id(stadium_id)
            if not stadium:
                # Este ValueError deve ser lançado diretamente, não capturado pelo "except Exception"
                raise ValueError(f"Estádio com ID {stadium_id} não encontrado.")
            return stadium
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao buscar estádio por ID: {e}")
        # Removido: except Exception as e: que estava capturando o ValueError e re-lançando

    def find_stadium_by_name(self, name: str) -> Stadium:
        """
        Encontra um estádio pelo seu nome.
        Levanta ValueError se o nome for inválido ou o estádio não for encontrado.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nome do estádio deve ser uma string não vazia.")
        
        normalized_name = name.strip()
        if len(normalized_name) < 3 or len(normalized_name) > 100:
            raise ValueError("Nome do estádio deve ter entre 3 e 100 caracteres.")

        try:
            stadium = self.repository.get_by_name(normalized_name)
            if not stadium:
                # Este ValueError deve ser lançado diretamente
                raise ValueError(f"Estádio com nome '{normalized_name}' não encontrado.")
            return stadium
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao buscar estádio por nome: {e}")
        # Removido: except Exception as e:

    def create_stadium(self, name: str, city: str, country_id: int) -> Stadium:
        """
        Cria um novo estádio.
        Realiza validações de entrada e trata erros de integridade.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Nome do estádio é obrigatório.")
        normalized_name = name.strip()
        if len(normalized_name) < 3 or len(normalized_name) > 100:
            raise ValueError("Nome do estádio deve ter entre 3 e 100 caracteres.")

        if not isinstance(city, str) or not city.strip():
            raise ValueError("Cidade do estádio é obrigatória.")
        normalized_city = city.strip()
        if len(normalized_city) < 2 or len(normalized_city) > 100:
            raise ValueError("Cidade do estádio deve ter entre 2 e 100 caracteres.")

        if not isinstance(country_id, int) or country_id < 1:
            raise ValueError("ID do país deve ser um número inteiro positivo.")
        
        try:
            stadium = self.repository.create(normalized_name, normalized_city, country_id)
            return stadium
        except IntegrityError as e:
            if "uq_stadium_name" in str(e) or "duplicate key value violates unique constraint" in str(e):
                raise ValueError(f"Já existe um estádio com o nome '{normalized_name}'.")
            raise ValueError(f"Erro de integridade ao criar estádio: {e}")
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao criar estádio: {e}")
        # Este bloco já estava bom, pois não esperava que ValuError fosse lançado aqui naturalmente
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado ao criar estádio: {e}")

    def get_all_stadiums(self) -> List[Stadium]:
        """
        Retorna todos os estádios.
        """
        try:
            return self.repository.get_all()
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao recuperar todos os estádios: {e}")
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado ao recuperar todos os estádios: {e}")

    def update_stadium(self, stadium_id: int, name: Optional[str] = None, 
                      city: Optional[str] = None, country_id: Optional[int] = None) -> Stadium:
        """
        Atualiza um estádio pelo seu ID.
        Realiza validações e trata erros de "não encontrado" e de integridade.
        """
        if not isinstance(stadium_id, int) or stadium_id < 1:
            raise ValueError("ID do estádio deve ser um número inteiro positivo.")

        existing_stadium = self.repository.get_by_id(stadium_id)
        if not existing_stadium:
            raise ValueError(f"Estádio com ID {stadium_id} não encontrado para atualização.")

        update_data = {}
        if name is not None:
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Nome do estádio não pode ser vazio ou inválido.")
            normalized_name = name.strip()
            if len(normalized_name) < 3 or len(normalized_name) > 100:
                raise ValueError("Nome do estádio deve ter entre 3 e 100 caracteres.")
            update_data['name'] = normalized_name

        if city is not None:
            if not isinstance(city, str) or not city.strip():
                raise ValueError("Cidade do estádio não pode ser vazia ou inválida.")
            normalized_city = city.strip()
            if len(normalized_city) < 2 or len(normalized_city) > 100:
                raise ValueError("Cidade do estádio deve ter entre 2 e 100 caracteres.")
            update_data['city'] = normalized_city

        if country_id is not None:
            if not isinstance(country_id, int) or country_id < 1:
                raise ValueError("ID do país deve ser um número inteiro positivo.")
            update_data['country_id'] = country_id
        
        if not update_data:
            return existing_stadium

        try:
            updated_stadium = self.repository.update(stadium_id, **update_data)
            if not updated_stadium:
                raise Exception(f"Falha ao atualizar o estádio com ID {stadium_id}.")
            return updated_stadium
        except IntegrityError as e:
            if "uq_stadium_name" in str(e) or "duplicate key value violates unique constraint" in str(e):
                raise ValueError(f"Já existe um estádio com o nome '{update_data.get('name')}' após a atualização.")
            raise ValueError(f"Erro de integridade ao atualizar estádio: {e}")
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao atualizar estádio: {e}")
        except Exception as e:
            raise Exception(f"Ocorreu um erro inesperado ao atualizar estádio: {e}")


    def delete_stadium(self, stadium_id: int) -> bool:
        """
        Exclui um estádio pelo seu ID.
        Levanta ValueError se o ID for inválido ou o estádio não for encontrado.
        """
        if not isinstance(stadium_id, int) or stadium_id < 1:
            raise ValueError("ID do estádio deve ser um número inteiro positivo.")

        try:
            stadium = self.repository.get_by_id(stadium_id)
            if not stadium:
                # Este ValueError deve ser lançado diretamente
                raise ValueError(f"Estádio com ID {stadium_id} não encontrado para exclusão.")
            
            return self.repository.delete(stadium_id)
        except SQLAlchemyError as e:
            raise Exception(f"Erro no banco de dados ao excluir estádio: {e}")
        # Removido: except Exception as e: