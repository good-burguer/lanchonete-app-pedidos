import pytest
from unittest.mock import MagicMock

from app.use_cases.status_pedido_use_case import StatusPedidoUseCase


@pytest.fixture
def mock_entity():
    return MagicMock()


def test_criar_retorna_schema(mock_entity):
    fake = MagicMock()
    fake.id = 1
    fake.descricao = "Pronto"

    mock_entity.criar.return_value = fake

    uc = StatusPedidoUseCase(mock_entity)
    result = uc.criar(MagicMock())

    assert result.id == fake.id
    assert result.descricao == fake.descricao


def test_buscar_por_id_levanta_404_quando_nao_encontrado(mock_entity):
    mock_entity.buscar_por_id.return_value = None

    uc = StatusPedidoUseCase(mock_entity)

    with pytest.raises(ValueError):
        uc.buscar_por_id(123)


def test_listar_todos_retorna_lista_de_schemas(mock_entity):
    fake1 = MagicMock(); fake1.id = 1; fake1.descricao = "A"
    fake2 = MagicMock(); fake2.id = 2; fake2.descricao = "B"
    mock_entity.listar_todos.return_value = [fake1, fake2]

    uc = StatusPedidoUseCase(mock_entity)
    result = uc.listar_todos()

    assert isinstance(result, list)
    assert result[0].id == 1


def test_atualizar_delega_e_retorna_schema(mock_entity):
    existing = MagicMock(); existing.id = 1; existing.descricao = "A"
    updated = MagicMock(); updated.id = 1; updated.descricao = "Updated"

    mock_entity.buscar_por_id.return_value = existing
    mock_entity.atualizar.return_value = updated

    uc = StatusPedidoUseCase(mock_entity)
    result = uc.atualizar(1, MagicMock())

    assert result.descricao == "Updated"
