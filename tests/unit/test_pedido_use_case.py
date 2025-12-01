import pytest
from unittest.mock import MagicMock
import datetime

from app.use_cases.pedido_use_case import PedidoUseCase
from app.adapters.dto.pedido_dto import PedidoAtualizaSchema


@pytest.fixture
def mock_entity():
    return MagicMock()


def test_criar_pedido_delega_e_prepara_response(mock_entity):
    fake_db_obj = MagicMock()
    fake_db_obj.id = 1
    fake_db_obj.cliente_id = 5
    fake_db_obj.status_rel = MagicMock()
    fake_db_obj.status_rel.id = 2
    fake_db_obj.status_rel.descricao = "Em preparo"
    fake_db_obj.data_criacao = datetime.time(10, 0, 0)
    fake_db_obj.data_alteracao = None
    fake_db_obj.data_finalizacao = None

    mock_entity.criar_pedido.return_value = fake_db_obj

    uc = PedidoUseCase(mock_entity)
    response = uc.criar_pedido(MagicMock())

    assert response.id == fake_db_obj.id
    assert response.cliente_id == fake_db_obj.cliente_id
    assert response.status.id == fake_db_obj.status_rel.id


def test_listar_todos_mapeia_respostas(mock_entity):
    fake_db_obj = MagicMock()
    fake_db_obj.id = 1
    fake_db_obj.cliente_id = 5
    fake_db_obj.status_rel = MagicMock()
    fake_db_obj.status_rel.id = 2
    fake_db_obj.status_rel.descricao = "Em preparo"

    mock_entity.listar_todos.return_value = [fake_db_obj]

    uc = PedidoUseCase(mock_entity)
    response = uc.listar_todos()

    assert isinstance(response, list)
    assert response[0].id == fake_db_obj.id


def test_buscar_por_id_levanta_404_quando_nao_encontrado(mock_entity):
    mock_entity.buscar_por_id.return_value = None

    uc = PedidoUseCase(mock_entity)

    with pytest.raises(ValueError):
        uc.buscar_por_id(999)


def test_atualizar_pedido_levanta_404_quando_nao_encontrado(mock_entity):
    mock_entity.atualizar_pedido.return_value = None

    uc = PedidoUseCase(mock_entity)

    with pytest.raises(ValueError):
        uc.atualizar_pedido(1, PedidoAtualizaSchema())
