import pytest
from unittest.mock import MagicMock, patch

from app.gateways.pedido_gateway import PedidoGateway


def test_criar_pedido_delega_para_dao():
    mock_dao = MagicMock()
    mock_dao.criar_pedido.return_value = MagicMock()

    with patch("app.gateways.pedido_gateway.PedidoDAO", return_value=mock_dao):
        gw = PedidoGateway(MagicMock())
        result = gw.criar_pedido(MagicMock())

    assert result == mock_dao.criar_pedido.return_value


def test_listar_todos_combina_tres_statuses():
    mock_dao = MagicMock()
    mock_dao.busca_por_status.side_effect = [[1], [2], [3]]

    with patch("app.gateways.pedido_gateway.PedidoDAO", return_value=mock_dao):
        gw = PedidoGateway(MagicMock())
        result = gw.listar_todos()

    assert result == [1,2,3]


def test_buscar_por_id_delega():
    mock_dao = MagicMock()
    mock_dao.buscar_por_id.return_value = MagicMock()

    with patch("app.gateways.pedido_gateway.PedidoDAO", return_value=mock_dao):
        gw = PedidoGateway(MagicMock())
        result = gw.buscar_por_id(1)

    assert result == mock_dao.buscar_por_id.return_value
