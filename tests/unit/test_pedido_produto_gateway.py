import pytest
from unittest.mock import MagicMock, patch

from app.gateways.pedido_produto_gateway import PedidoProdutoGateway


def test_criarPedidoProduto_delega_para_dao():
    mock_dao = MagicMock()
    mock_dao.criar_pedido_produto.return_value = MagicMock()

    with patch("app.gateways.pedido_produto_gateway.PedidoProdutoDAO", return_value=mock_dao):
        gw = PedidoProdutoGateway(MagicMock())
        result = gw.criarPedidoProduto(1, 2)

    assert result == mock_dao.criar_pedido_produto.return_value


def test_buscarPorIdPedido_delega():
    mock_dao = MagicMock()
    mock_dao.buscarPorIdPedido.return_value = [MagicMock()]

    with patch("app.gateways.pedido_produto_gateway.PedidoProdutoDAO", return_value=mock_dao):
        gw = PedidoProdutoGateway(MagicMock())
        result = gw.buscarPorIdPedido(1)

    assert result == mock_dao.buscarPorIdPedido.return_value


def test_deletar_delega():
    mock_dao = MagicMock()
    with patch("app.gateways.pedido_produto_gateway.PedidoProdutoDAO", return_value=mock_dao):
        gw = PedidoProdutoGateway(MagicMock())
        gw.deletar(1)

    mock_dao.deletar.assert_called_with(1)
