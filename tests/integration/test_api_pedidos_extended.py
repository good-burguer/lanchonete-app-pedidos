"""Extended integration tests for pedidos API endpoints"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi.testclient import TestClient
from app.infrastructure.api.fastapi import app
from app.api import pedido as pedido_api
from tests.integration.conftest import FakePedido

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_overrides():
    """Clean up dependency overrides after each test."""
    yield
    app.dependency_overrides.clear()


class TestPedidosCreateEndpoint:
    """Tests for POST /pedidos/ endpoint"""
    
    def test_criar_pedido_with_error_in_gateway(self):
        """Test criar_pedido when gateway raises exception"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.criar_pedido.side_effect = Exception("Database error")

        mock_pedido_prod_gateway = MagicMock()

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        payload = {"cliente_id": 1, "produtos": [1, 2]}

        res = client.post("/pedidos/", json=payload)
        assert res.status_code == 400

    def test_criar_pedido_with_invalid_schema(self):
        """Test criar_pedido with invalid request schema"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_prod_gateway = MagicMock()

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        payload = {"invalid_field": "value"}  # Missing required fields

        res = client.post("/pedidos/", json=payload)
        assert res.status_code == 422


class TestPedidosListEndpoint:
    """Tests for GET /pedidos/ endpoint"""
    
    def test_listar_pedidos_with_error(self):
        """Test list pedidos when gateway raises exception"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.listar_todos.side_effect = Exception("Database connection error")

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway

        res = client.get("/pedidos/")
        assert res.status_code == 400

    def test_listar_pedidos_empty(self):
        """Test listing when no pedidos exist"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.listar_todos.return_value = []

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway

        res = client.get("/pedidos/")
        assert res.status_code == 200
        body = res.json()
        assert len(body["data"]) == 0


class TestPedidosGetByIdEndpoint:
    """Tests for GET /pedidos/{id} endpoint"""
    
    def test_buscar_pedido_success(self, fake_pedido):
        """Test successfully fetching a pedido by id"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.buscar_por_id.return_value = fake_pedido

        mock_pedido_prod_gateway = MagicMock()
        mock_pedido_prod_gateway.buscarPorIdPedido.return_value = [
            MagicMock(produto_id=1),
            MagicMock(produto_id=2)
        ]

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        res = client.get("/pedidos/1")
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "success"
        assert body["data"]["id"] == fake_pedido.id

    def test_buscar_pedido_with_general_exception(self):
        """Test buscar_pedido with general exception"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.buscar_por_id.side_effect = Exception("Unexpected error")

        mock_pedido_prod_gateway = MagicMock()

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        res = client.get("/pedidos/999")
        assert res.status_code == 400


class TestPedidosUpdateEndpoint:
    """Tests for PUT /pedidos/{id} endpoint"""
    
    def test_atualizar_pedido_success(self, fake_pedido):
        """Test successfully updating a pedido"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.atualizar_pedido.return_value = fake_pedido

        mock_pedido_prod_gateway = MagicMock()
        mock_pedido_prod_gateway.buscarPorIdPedido.return_value = [MagicMock(produto_id=1)]

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        payload = {"status": "2"}

        res = client.put("/pedidos/1", json=payload)
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "success"

    def test_atualizar_pedido_not_found(self):
        """Test updating a pedido that does not exist"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.atualizar_pedido.side_effect = ValueError("Pedido não encontrado")

        mock_pedido_prod_gateway = MagicMock()

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        payload = {"status": "2"}

        res = client.put("/pedidos/999", json=payload)
        assert res.status_code == 404

    def test_atualizar_pedido_with_error(self):
        """Test updating a pedido with general error"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.atualizar_pedido.side_effect = Exception("Database error")

        mock_pedido_prod_gateway = MagicMock()

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        payload = {"status": "2"}

        res = client.put("/pedidos/1", json=payload)
        assert res.status_code == 400


class TestPedidosDeleteEndpoint:
    """Tests for DELETE /pedidos/{id} endpoint"""
    
    def test_deletar_pedido_success(self):
        """Test successfully deleting a pedido"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_prod_gateway = MagicMock()

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        res = client.delete("/pedidos/1")
        assert res.status_code == 204

    def test_deletar_pedido_not_found(self):
        """Test deleting a pedido that does not exist"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.deletar_pedido.side_effect = ValueError("Pedido não encontrado")

        mock_pedido_prod_gateway = MagicMock()
        mock_pedido_prod_gateway.deletarPorPedido.side_effect = ValueError("Pedido não encontrado")

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        res = client.delete("/pedidos/999")
        assert res.status_code == 404

    def test_deletar_pedido_with_error(self):
        """Test deleting a pedido with general error"""
        mock_pedido_gateway = MagicMock()
        mock_pedido_gateway.deletar_pedido.side_effect = Exception("Database error")

        mock_pedido_prod_gateway = MagicMock()

        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: mock_pedido_gateway
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: mock_pedido_prod_gateway

        res = client.delete("/pedidos/1")
        assert res.status_code == 400
