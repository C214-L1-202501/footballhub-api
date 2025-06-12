import pytest
from unittest.mock import MagicMock
from app.services.StadiumService import StadiumService
from app.schemas.stadium import Stadium # Certifique-se de que seu esquema Stadium é importável

# Fixture para mockar o StadiumRepository
@pytest.fixture
def mock_stadium_repository():
    return MagicMock()

# Fixture para o StadiumService, injetando o mock do repositório
@pytest.fixture
def stadium_service(mock_stadium_repository):
    return StadiumService(stadium_repository=mock_stadium_repository)

# --- Testes para find_stadium_by_id ---
def test_find_stadium_by_id_success(stadium_service, mock_stadium_repository):
    # Configurar o mock para retornar um estádio
    mock_stadium_repository.get_by_id.return_value = Stadium(
        id=1, name="Maracanã", city="Rio de Janeiro", country_id=1
    )
    
    stadium = stadium_service.find_stadium_by_id(1)
    
    # Verificar que o estádio foi retornado e o método do repositório foi chamado
    assert stadium.name == "Maracanã"
    mock_stadium_repository.get_by_id.assert_called_once_with(1)

def test_find_stadium_by_id_not_found(stadium_service, mock_stadium_repository):
    # Configurar o mock para retornar None (estádio não encontrado)
    mock_stadium_repository.get_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Estádio com ID 999 não encontrado."):
        stadium_service.find_stadium_by_id(999)
    
    mock_stadium_repository.get_by_id.assert_called_once_with(999)

def test_find_stadium_by_id_invalid_id_type(stadium_service):
    with pytest.raises(ValueError, match="ID do estádio deve ser um número inteiro positivo."):
        stadium_service.find_stadium_by_id("abc") # ID inválido (string)

def test_find_stadium_by_id_invalid_id_value(stadium_service):
    with pytest.raises(ValueError, match="ID do estádio deve ser um número inteiro positivo."):
        stadium_service.find_stadium_by_id(0) # ID inválido (zero)
    with pytest.raises(ValueError, match="ID do estádio deve ser um número inteiro positivo."):
        stadium_service.find_stadium_by_id(-5) # ID inválido (negativo)

def test_find_stadium_by_id_repository_error(stadium_service, mock_stadium_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_stadium_repository.get_by_id.side_effect = SQLAlchemyError("Database connection lost")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao buscar estádio por ID:"):
        stadium_service.find_stadium_by_id(1)

# --- Testes para find_stadium_by_name ---
def test_find_stadium_by_name_success(stadium_service, mock_stadium_repository):
    mock_stadium_repository.get_by_name.return_value = Stadium(
        id=1, name="Allianz Parque", city="São Paulo", country_id=1
    )
    
    stadium = stadium_service.find_stadium_by_name("Allianz Parque")
    
    assert stadium.name == "Allianz Parque"
    mock_stadium_repository.get_by_name.assert_called_once_with("Allianz Parque")

def test_find_stadium_by_name_not_found(stadium_service, mock_stadium_repository):
    mock_stadium_repository.get_by_name.return_value = None
    
    with pytest.raises(ValueError, match="Estádio com nome 'Estádio Inexistente' não encontrado."):
        stadium_service.find_stadium_by_name("Estádio Inexistente")
    
    mock_stadium_repository.get_by_name.assert_called_once_with("Estádio Inexistente")

def test_find_stadium_by_name_invalid_name(stadium_service):
    with pytest.raises(ValueError, match="Nome do estádio deve ser uma string não vazia."):
        stadium_service.find_stadium_by_name("")
    with pytest.raises(ValueError, match="Nome do estádio deve ser uma string não vazia."):
        stadium_service.find_stadium_by_name("   ")
    with pytest.raises(ValueError, match="Nome do estádio deve ser uma string não vazia."):
        stadium_service.find_stadium_by_name(None)
    with pytest.raises(ValueError, match="Nome do estádio deve ser uma string não vazia."):
        stadium_service.find_stadium_by_name(123)

def test_find_stadium_by_name_name_too_short(stadium_service):
    with pytest.raises(ValueError, match="Nome do estádio deve ter entre 3 e 100 caracteres."):
        stadium_service.find_stadium_by_name("ab")

def test_find_stadium_by_name_name_too_long(stadium_service):
    with pytest.raises(ValueError, match="Nome do estádio deve ter entre 3 e 100 caracteres."):
        stadium_service.find_stadium_by_name("a" * 101)

def test_find_stadium_by_name_repository_error(stadium_service, mock_stadium_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_stadium_repository.get_by_name.side_effect = SQLAlchemyError("Network error during fetch")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao buscar estádio por nome:"):
        stadium_service.find_stadium_by_name("Nome Qualquer")

# --- Testes para create_stadium ---
def test_create_stadium_success(stadium_service, mock_stadium_repository):
    mock_stadium_repository.create.return_value = Stadium(
        id=1, name="Arena Corinthians", city="São Paulo", country_id=1
    )
    
    stadium = stadium_service.create_stadium("Arena Corinthians", "São Paulo", 1)
    
    assert stadium.name == "Arena Corinthians"
    mock_stadium_repository.create.assert_called_once_with("Arena Corinthians", "São Paulo", 1)

def test_create_stadium_invalid_name(stadium_service):
    with pytest.raises(ValueError, match="Nome do estádio é obrigatório."):
        stadium_service.create_stadium("", "City", 1)
    with pytest.raises(ValueError, match="Nome do estádio é obrigatório."):
        stadium_service.create_stadium("   ", "City", 1)
    with pytest.raises(ValueError, match="Nome do estádio é obrigatório."):
        stadium_service.create_stadium(None, "City", 1)
    with pytest.raises(ValueError, match="Nome do estádio deve ter entre 3 e 100 caracteres."):
        stadium_service.create_stadium("a", "City", 1)
    with pytest.raises(ValueError, match="Nome do estádio deve ter entre 3 e 100 caracteres."):
        stadium_service.create_stadium("a"*101, "City", 1)

def test_create_stadium_invalid_city(stadium_service):
    with pytest.raises(ValueError, match="Cidade do estádio é obrigatória."):
        stadium_service.create_stadium("Stadium Name", "", 1)
    with pytest.raises(ValueError, match="Cidade do estádio é obrigatória."):
        stadium_service.create_stadium("Stadium Name", "   ", 1)
    with pytest.raises(ValueError, match="Cidade do estádio é obrigatória."):
        stadium_service.create_stadium("Stadium Name", None, 1)
    with pytest.raises(ValueError, match="Cidade do estádio deve ter entre 2 e 100 caracteres."):
        stadium_service.create_stadium("Stadium Name", "a", 1)
    with pytest.raises(ValueError, match="Cidade do estádio deve ter entre 2 e 100 caracteres."):
        stadium_service.create_stadium("Stadium Name", "a"*101, 1)

def test_create_stadium_invalid_country_id(stadium_service):
    with pytest.raises(ValueError, match="ID do país deve ser um número inteiro positivo."):
        stadium_service.create_stadium("Stadium Name", "City", 0)
    with pytest.raises(ValueError, match="ID do país deve ser um número inteiro positivo."):
        stadium_service.create_stadium("Stadium Name", "City", -1)
    with pytest.raises(ValueError, match="ID do país deve ser um número inteiro positivo."):
        stadium_service.create_stadium("Stadium Name", "City", "abc")

def test_create_stadium_integrity_error_duplicate_name(stadium_service, mock_stadium_repository):
    from sqlalchemy.exc import IntegrityError
    mock_stadium_repository.create.side_effect = IntegrityError("duplicate key value violates unique constraint \"uq_stadium_name\"", [], None)
    
    with pytest.raises(ValueError, match="Já existe um estádio com o nome 'Estádio Duplicado'."):
        stadium_service.create_stadium("Estádio Duplicado", "Cidade", 1)

def test_create_stadium_repository_error(stadium_service, mock_stadium_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_stadium_repository.create.side_effect = SQLAlchemyError("DB connection error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao criar estádio:"):
        stadium_service.create_stadium("Estádio Teste", "Cidade Teste", 1)

# --- Testes para get_all_stadiums ---
def test_get_all_stadiums_success(stadium_service, mock_stadium_repository):
    mock_stadium_repository.get_all.return_value = [
        Stadium(id=1, name="S1", city="C1", country_id=1),
        Stadium(id=2, name="S2", city="C2", country_id=1)
    ]
    
    stadiums = stadium_service.get_all_stadiums()
    
    assert len(stadiums) == 2
    assert stadiums[0].name == "S1"
    mock_stadium_repository.get_all.assert_called_once()

def test_get_all_stadiums_empty(stadium_service, mock_stadium_repository):
    mock_stadium_repository.get_all.return_value = []
    
    stadiums = stadium_service.get_all_stadiums()
    
    assert len(stadiums) == 0
    mock_stadium_repository.get_all.assert_called_once()

def test_get_all_stadiums_repository_error(stadium_service, mock_stadium_repository):
    from sqlalchemy.exc import SQLAlchemyError
    mock_stadium_repository.get_all.side_effect = SQLAlchemyError("DB error during fetch all")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao recuperar todos os estádios:"):
        stadium_service.get_all_stadiums()

# --- Testes para update_stadium ---
@pytest.fixture
def existing_stadium():
    return Stadium(id=1, name="Old Name", city="Old City", country_id=1)

def test_update_stadium_success_name_only(stadium_service, mock_stadium_repository, existing_stadium):
    mock_stadium_repository.get_by_id.return_value = existing_stadium
    updated_stadium_mock = Stadium(id=1, name="New Name", city="Old City", country_id=1)
    mock_stadium_repository.update.return_value = updated_stadium_mock
    
    stadium = stadium_service.update_stadium(1, name="New Name")
    
    assert stadium.name == "New Name"
    assert stadium.city == "Old City" # Cidade não foi alterada
    mock_stadium_repository.get_by_id.assert_called_once_with(1)
    mock_stadium_repository.update.assert_called_once_with(1, name="New Name")

def test_update_stadium_success_all_fields(stadium_service, mock_stadium_repository, existing_stadium):
    mock_stadium_repository.get_by_id.return_value = existing_stadium
    updated_stadium_mock = Stadium(id=1, name="Updated Name", city="Updated City", country_id=2)
    mock_stadium_repository.update.return_value = updated_stadium_mock
    
    stadium = stadium_service.update_stadium(1, name="Updated Name", city="Updated City", country_id=2)
    
    assert stadium.name == "Updated Name"
    assert stadium.city == "Updated City"
    assert stadium.country_id == 2
    mock_stadium_repository.get_by_id.assert_called_once_with(1)
    mock_stadium_repository.update.assert_called_once_with(1, name="Updated Name", city="Updated City", country_id=2)

def test_update_stadium_no_changes(stadium_service, mock_stadium_repository, existing_stadium):
    mock_stadium_repository.get_by_id.return_value = existing_stadium
    
    stadium = stadium_service.update_stadium(1) # Nenhuma alteração passada
    
    assert stadium == existing_stadium # Retorna o objeto existente sem chamar update
    mock_stadium_repository.get_by_id.assert_called_once_with(1)
    mock_stadium_repository.update.assert_not_called()

def test_update_stadium_not_found(stadium_service, mock_stadium_repository):
    mock_stadium_repository.get_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Estádio com ID 999 não encontrado para atualização."):
        stadium_service.update_stadium(999, name="New Name")
    
    mock_stadium_repository.get_by_id.assert_called_once_with(999)
    mock_stadium_repository.update.assert_not_called()

def test_update_stadium_invalid_id(stadium_service):
    with pytest.raises(ValueError, match="ID do estádio deve ser um número inteiro positivo."):
        stadium_service.update_stadium("abc", name="New Name")
    with pytest.raises(ValueError, match="ID do estádio deve ser um número inteiro positivo."):
        stadium_service.update_stadium(0, name="New Name")

def test_update_stadium_invalid_name(stadium_service, mock_stadium_repository, existing_stadium):
    mock_stadium_repository.get_by_id.return_value = existing_stadium
    with pytest.raises(ValueError, match="Nome do estádio não pode ser vazio ou inválido."):
        stadium_service.update_stadium(1, name="  ")
    with pytest.raises(ValueError, match="Nome do estádio deve ter entre 3 e 100 caracteres."):
        stadium_service.update_stadium(1, name="a")
    mock_stadium_repository.update.assert_not_called()

def test_update_stadium_invalid_city(stadium_service, mock_stadium_repository, existing_stadium):
    mock_stadium_repository.get_by_id.return_value = existing_stadium
    with pytest.raises(ValueError, match="Cidade do estádio não pode ser vazia ou inválida."):
        stadium_service.update_stadium(1, city="  ")
    with pytest.raises(ValueError, match="Cidade do estádio deve ter entre 2 e 100 caracteres."):
        stadium_service.update_stadium(1, city="a")
    mock_stadium_repository.update.assert_not_called()

def test_update_stadium_invalid_country_id(stadium_service, mock_stadium_repository, existing_stadium):
    mock_stadium_repository.get_by_id.return_value = existing_stadium
    with pytest.raises(ValueError, match="ID do país deve ser um número inteiro positivo."):
        stadium_service.update_stadium(1, country_id=0)
    mock_stadium_repository.update.assert_not_called()

def test_update_stadium_integrity_error_duplicate_name(stadium_service, mock_stadium_repository, existing_stadium):
    from sqlalchemy.exc import IntegrityError
    mock_stadium_repository.get_by_id.return_value = existing_stadium
    mock_stadium_repository.update.side_effect = IntegrityError("duplicate key value violates unique constraint \"uq_stadium_name\"", [], None)
    
    with pytest.raises(ValueError, match="Já existe um estádio com o nome 'Existing Stadium' após a atualização."):
        stadium_service.update_stadium(1, name="Existing Stadium")
    mock_stadium_repository.update.assert_called_once()

def test_update_stadium_repository_error(stadium_service, mock_stadium_repository, existing_stadium):
    from sqlalchemy.exc import SQLAlchemyError
    mock_stadium_repository.get_by_id.return_value = existing_stadium
    mock_stadium_repository.update.side_effect = SQLAlchemyError("DB update error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao atualizar estádio:"):
        stadium_service.update_stadium(1, name="New Name")
    mock_stadium_repository.update.assert_called_once()

# --- Testes para delete_stadium ---
def test_delete_stadium_success(stadium_service, mock_stadium_repository):
    mock_stadium_repository.get_by_id.return_value = Stadium(id=1, name="To Delete", city="City", country_id=1)
    mock_stadium_repository.delete.return_value = True
    
    result = stadium_service.delete_stadium(1)
    
    assert result is True
    mock_stadium_repository.get_by_id.assert_called_once_with(1)
    mock_stadium_repository.delete.assert_called_once_with(1)

def test_delete_stadium_not_found(stadium_service, mock_stadium_repository):
    mock_stadium_repository.get_by_id.return_value = None
    
    with pytest.raises(ValueError, match="Estádio com ID 999 não encontrado para exclusão."):
        stadium_service.delete_stadium(999)
    
    mock_stadium_repository.get_by_id.assert_called_once_with(999)
    mock_stadium_repository.delete.assert_not_called()

def test_delete_stadium_invalid_id(stadium_service):
    with pytest.raises(ValueError, match="ID do estádio deve ser um número inteiro positivo."):
        stadium_service.delete_stadium("abc")
    with pytest.raises(ValueError, match="ID do estádio deve ser um número inteiro positivo."):
        stadium_service.delete_stadium(0)

def test_delete_stadium_repository_error(stadium_service, mock_stadium_repository):
    mock_stadium_repository.get_by_id.return_value = Stadium(id=1, name="To Delete", city="City", country_id=1)
    from sqlalchemy.exc import SQLAlchemyError
    mock_stadium_repository.delete.side_effect = SQLAlchemyError("DB delete error")
    
    with pytest.raises(Exception, match="Erro no banco de dados ao excluir estádio:"):
        stadium_service.delete_stadium(1)
    mock_stadium_repository.get_by_id.assert_called_once_with(1)
    mock_stadium_repository.delete.assert_called_once_with(1)