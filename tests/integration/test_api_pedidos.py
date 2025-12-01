from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest

from app.infrastructure.api.fastapi import app
from app.api import pedido as pedido_api
from tests.integration.conftest import FakePedido
from app.adapters.utils.debug import var_dump_die

# include router for tests
app.include_router(pedido_api.router)
client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_overrides():
    """Clean up dependency overrides after each test."""
    yield
    app.dependency_overrides.clear()


def test_criar_pedido_success(fake_pedido):
    # mock gateways
    mock_pedido_gateway = MagicMock()
    mock_pedido_gateway.criar_pedido.return_value = fake_pedido

    mock_pedido_prod_gateway = MagicMock()
    mock_pedido_prod_gateway.buscarPorIdPedido.return_value = [MagicMock(produto_id=1), MagicMock(produto_id=2)]

    app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
    app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

    payload = {"cliente_id": 1, "produtos": [1, 2, 3]}

    res = client.post("/pedidos/", json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "success"
    assert body["data"]["id"] == fake_pedido.id
    assert body["data"]["produtos"] == [1, 2]


def test_listar_pedidos_success(fake_pedido):
    p2 = FakePedido(id=2, cliente_id=43)
    mock_pedido_gateway = MagicMock()
    mock_pedido_gateway.listar_todos.return_value = [fake_pedido, p2]

    app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway

    res = client.get("/pedidos/")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] in ("success", "sucess")
    assert len(body["data"]) == 2


def test_buscar_pedido_not_found():
    mock_pedido_gateway = MagicMock()
    mock_pedido_gateway.buscar_por_id.side_effect = ValueError("Pedido não encontrado")

    app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
    app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: MagicMock()

    res = client.get("/pedidos/999")

    assert res.status_code == 400
