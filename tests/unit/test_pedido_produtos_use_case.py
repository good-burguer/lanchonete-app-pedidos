import pytest
from unittest.mock import MagicMock

from app.use_cases.pedido_produtos_use_case import PedidoProdutosUseCase


@pytest.fixture
def mock_gateway():
    return MagicMock()


def test_criar_pedido_produtos_delega_e_retornas_lista(mock_gateway):
    item1 = MagicMock(); item1.produto_id = 10
    item2 = MagicMock(); item2.produto_id = 20
    mock_gateway.buscarPorIdPedido.return_value = [item1, item2]

    uc = PedidoProdutosUseCase(mock_gateway)
    result = uc.criarPedidoProdutos(1, [10, 20])

    assert result == [10, 20]
    mock_gateway.criarPedidoProduto.assert_called()


def test_buscarPorIdPedido_retorna_lista_de_ids(mock_gateway):
    item1 = MagicMock(); item1.produto_id = 7
    mock_gateway.buscarPorIdPedido.return_value = [item1]

    uc = PedidoProdutosUseCase(mock_gateway)
    result = uc.buscarPorIdPedido(1)

    assert result == [7]


def test_deletarPorPedido_deleta_cada_item(mock_gateway):
    p1 = MagicMock(); p1.id = 1
    p2 = MagicMock(); p2.id = 2
    mock_gateway.buscarPorIdPedido.return_value = [p1, p2]

    uc = PedidoProdutosUseCase(mock_gateway)
    uc.deletarPorPedido(1)

    assert mock_gateway.deletar.call_count == 2
