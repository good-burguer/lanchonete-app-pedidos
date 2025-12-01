import pytest
from unittest.mock import MagicMock, patch

from app.gateways.status_pedido_gateway import StatusPedidoGateway


def test_criar_delega_para_dao():
    mock_dao = MagicMock()
    mock_dao.criar.return_value = MagicMock()

    with patch("app.gateways.status_pedido_gateway.StatusPedidoDAO", return_value=mock_dao):
        gw = StatusPedidoGateway(MagicMock())
        result = gw.criar(MagicMock())

    assert result == mock_dao.criar.return_value


def test_buscar_por_id_delega_e_retorna_none_quando_nao_existe():
    mock_dao = MagicMock()
    mock_dao.buscar_por_id.return_value = None

    with patch("app.gateways.status_pedido_gateway.StatusPedidoDAO", return_value=mock_dao):
        gw = StatusPedidoGateway(MagicMock())
        result = gw.buscar_por_id(1)

    assert result is None


def test_listar_todos_delega():
    mock_dao = MagicMock()
    mock_dao.listar_todos.return_value = [MagicMock(), MagicMock()]

    with patch("app.gateways.status_pedido_gateway.StatusPedidoDAO", return_value=mock_dao):
        gw = StatusPedidoGateway(MagicMock())
        result = gw.listar_todos()

    assert isinstance(result, list)
