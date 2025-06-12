from typing import List, Optional
from app.schemas.championship import Championship
from app.repositories.championshipRepository import ChampionshipRepository


class ChampionshipService:
    def __init__(self, championship_repository: ChampionshipRepository = None):
        self.repository = championship_repository if championship_repository else ChampionshipRepository()

    def find_championship_by_id(self, championship_id: int) -> Championship:
        try:
            championship = self.repository.get_by_id(championship_id)
            if not championship:
                raise ValueError("Campeonato não encontrado.")
        except Exception as e:
            raise e
        return championship
    
    def find_championship_by_name(self, name: str) -> Championship:
        try:
            championship = self.repository.get_by_name(name)
            if not championship:
                raise ValueError("Campeonato não encontrado.")
        except Exception as e:
            raise e
        return championship

    def create_championship(self, name: str, country_id: Optional[int], type: Optional[str], season: Optional[str]) -> Championship:
        if not name:
            raise ValueError("Championship name cannot be empty.")
        if not isinstance(name, str):
            raise ValueError("Championship name must be a string.")
        if len(name) > 100:
            raise ValueError("Championship name cannot exceed 100 characters.")
        
        existing_championship = self.repository.get_by_name(name)
        if existing_championship:
            raise ValueError("Championship with this name already exists.")

        championship = self.repository.create(name, country_id, type, season)
        return championship

    def get_all_championships(self) -> List[Championship]:
        return self.repository.get_all()

    def update_championship(self, championship_id: int, name: Optional[str] = None, country_id: Optional[int] = None,
                            type: Optional[str] = None, season: Optional[str] = None) -> Championship:
        
        championship = self.repository.get_by_id(championship_id) # Buscar o campeonato primeiro
        if not championship:
            raise ValueError("Campeonato não encontrado.")
        
        # Aplicar validações de nome se um novo nome for fornecido
        if name is not None: # Verifica se 'name' foi explicitamente passado (pode ser string vazia)
            if not name: # Se for string vazia
                raise ValueError("Championship name cannot be empty.")
            if not isinstance(name, str):
                raise ValueError("Championship name must be a string.")
            if len(name) > 100:
                raise ValueError("Championship name cannot exceed 100 characters.")
            
            # Se o nome for alterado, verificar se o novo nome já existe (apenas se for diferente do nome atual)
            if name != championship.name:
                existing_championship_with_new_name = self.repository.get_by_name(name)
                if existing_championship_with_new_name and existing_championship_with_new_name.id != championship_id:
                    raise ValueError("Championship with this name already exists.")

        updated_championship = self.repository.update(championship_id, name, country_id, type, season)
        
        # A verificação 'if not updated_championship' aqui é redundante se o get_by_id já validou a existência
        # mas pode ser útil se o método update do repo puder retornar None por outros motivos.
        # Por enquanto, vou manter já que seus testes esperavam isso inicialmente.
        if not updated_championship:
            raise ValueError("Erro ao atualizar o campeonato.") # Mensagem mais genérica se a atualização falhar no repo
            
        return updated_championship

    def delete_championship(self, championship_id: int) -> bool:
        championship = self.repository.get_by_id(championship_id)
        if not championship:
            raise ValueError("Campeonato não encontrado.")
        return self.repository.delete(championship_id)