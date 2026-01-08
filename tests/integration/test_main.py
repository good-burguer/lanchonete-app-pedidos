"""Tests for app.main module"""

import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from fastapi.testclient import TestClient
from app.infrastructure.api.fastapi import app

client = TestClient(app)


def test_app_includes_health_check_router():
    """Test that health check endpoint is available"""
    response = client.get("/health")
    assert response.status_code == 200


def test_app_includes_pedidos_router():
    """Test that pedidos endpoints are available"""
    response = client.get("/pedidos/")
    # Should return 500 or 400 or similar if DB is not set up,
    # but the route should exist (not 404)
    assert response.status_code != 404


def test_app_includes_status_pedido_router():
    """Test that status_pedido endpoints are available"""
    response = client.get("/status_pedido/")
    # Should return 500 or 400 or similar if DB is not set up,
    # but the route should exist (not 404)
    assert response.status_code != 404
