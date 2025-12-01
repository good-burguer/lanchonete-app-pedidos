from fastapi.testclient import TestClient
from unittest.mock import MagicMock
import pytest

from app.infrastructure.api.fastapi import app
from app.api import status_pedido as status_api
from tests.integration.conftest import FakeStatus

app.include_router(status_api.router)
client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_overrides():
    yield
    app.dependency_overrides.clear()


def test_criar_status_success(fake_status):
    mock_gateway = MagicMock()
    mock_gateway.criar.return_value = fake_status

    app.dependency_overrides[status_api.get_status_repository] = lambda: mock_gateway

    payload = {"descricao": "Pronto"}
    res = client.post("/status_pedido/", json=payload)

    assert res.status_code == 201
    body = res.json()
    assert body["status"] == "success"
    assert body["data"]["id"] == 1


def test_buscar_status_not_found():
    mock_gateway = MagicMock()
    mock_gateway.buscar_por_id.side_effect = ValueError("Status não encontrado")

    app.dependency_overrides[status_api.get_status_repository] = lambda: mock_gateway

    res = client.get("/status_pedido/999")
    assert res.status_code == 400
