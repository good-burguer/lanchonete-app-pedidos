"""Extended integration tests for status_pedido API endpoints"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi.testclient import TestClient
from app.infrastructure.api.fastapi import app
from app.api import status_pedido as status_pedido_api
from tests.integration.conftest import FakeStatus

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_overrides():
    """Clean up dependency overrides after each test."""
    yield
    app.dependency_overrides.clear()


class TestStatusPedidoCreateEndpoint:
    """Tests for POST /status_pedido/ endpoint"""
    
    def test_criar_status_success(self, fake_status):
        """Test successfully creating a status"""
        mock_gateway = MagicMock()
        mock_gateway.criar.return_value = fake_status

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        payload = {"descricao": "Novo Status"}

        res = client.post("/status_pedido/", json=payload)
        assert res.status_code == 201
        body = res.json()
        assert body["status"] == "success"

    def test_criar_status_with_error(self):
        """Test creating status when gateway raises exception"""
        mock_gateway = MagicMock()
        mock_gateway.criar.side_effect = Exception("Database error")

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        payload = {"descricao": "Novo Status"}

        res = client.post("/status_pedido/", json=payload)
        assert res.status_code == 400

    def test_criar_status_with_invalid_schema(self):
        """Test creating status with invalid schema"""
        mock_gateway = MagicMock()

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        payload = {}  # Missing required fields

        res = client.post("/status_pedido/", json=payload)
        assert res.status_code == 422


class TestStatusPedidoGetByIdEndpoint:
    """Tests for GET /status_pedido/{id} endpoint"""
    
    def test_buscar_status_success(self, fake_status):
        """Test successfully fetching a status by id"""
        mock_gateway = MagicMock()
        mock_gateway.buscar_por_id.return_value = fake_status

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        res = client.get("/status_pedido/1")
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "success"
        assert body["data"]["id"] == fake_status.id

    def test_buscar_status_not_found(self):
        """Test fetching a status that does not exist"""
        mock_gateway = MagicMock()
        mock_gateway.buscar_por_id.side_effect = ValueError("Status não encontrado")

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        res = client.get("/status_pedido/999")
        assert res.status_code == 404

    def test_buscar_status_with_error(self):
        """Test fetching status with general error"""
        mock_gateway = MagicMock()
        mock_gateway.buscar_por_id.side_effect = Exception("Database error")

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        res = client.get("/status_pedido/1")
        assert res.status_code == 400


class TestStatusPedidoListEndpoint:
    """Tests for GET /status_pedido/ endpoint"""
    
    def test_listar_status_success(self, fake_status):
        """Test successfully listing all statuses"""
        mock_gateway = MagicMock()
        mock_gateway.listar_todos.return_value = [fake_status]

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        res = client.get("/status_pedido/")
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "success"
        assert len(body["data"]) == 1

    def test_listar_status_empty(self):
        """Test listing when no statuses exist"""
        mock_gateway = MagicMock()
        mock_gateway.listar_todos.return_value = []

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        res = client.get("/status_pedido/")
        assert res.status_code == 200
        body = res.json()
        assert len(body["data"]) == 0

    def test_listar_status_with_error(self):
        """Test listing statuses with error"""
        mock_gateway = MagicMock()
        mock_gateway.listar_todos.side_effect = Exception("Database error")

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        res = client.get("/status_pedido/")
        assert res.status_code == 400


class TestStatusPedidoUpdateEndpoint:
    """Tests for PUT /status_pedido/{id} endpoint"""
    
    def test_atualizar_status_success(self, fake_status):
        """Test successfully updating a status"""
        mock_gateway = MagicMock()
        mock_gateway.atualizar.return_value = fake_status

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        payload = {"descricao": "Status Atualizado"}

        res = client.put("/status_pedido/1", json=payload)
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "success"

    def test_atualizar_status_not_found(self):
        """Test updating a status that does not exist"""
        mock_gateway = MagicMock()
        mock_gateway.atualizar.side_effect = ValueError("Status não encontrado")

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        payload = {"descricao": "Status Atualizado"}

        res = client.put("/status_pedido/999", json=payload)
        assert res.status_code == 404

    def test_atualizar_status_with_error(self):
        """Test updating status with general error"""
        mock_gateway = MagicMock()
        mock_gateway.atualizar.side_effect = Exception("Database error")

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        payload = {"descricao": "Status Atualizado"}

        res = client.put("/status_pedido/1", json=payload)
        assert res.status_code == 400


class TestStatusPedidoDeleteEndpoint:
    """Tests for DELETE /status_pedido/{id} endpoint"""
    
    def test_deletar_status_success(self):
        """Test successfully deleting a status"""
        mock_gateway = MagicMock()

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        res = client.delete("/status_pedido/1")
        assert res.status_code == 204

    def test_deletar_status_not_found(self):
        """Test deleting a status that does not exist"""
        mock_gateway = MagicMock()
        mock_gateway.deletar.side_effect = ValueError("Status não encontrado")

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        res = client.delete("/status_pedido/999")
        assert res.status_code == 404

    def test_deletar_status_with_error(self):
        """Test deleting status with general error"""
        mock_gateway = MagicMock()
        mock_gateway.deletar.side_effect = Exception("Database error")

        app.dependency_overrides[status_pedido_api.get_status_repository] = lambda: mock_gateway

        res = client.delete("/status_pedido/1")
        assert res.status_code == 400
