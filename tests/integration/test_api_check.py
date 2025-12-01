from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.infrastructure.api.fastapi import app
from app.api import check as check_api


app.include_router(check_api.router)

client = TestClient(app)


def test_health_check():
    res = client.get("/health/")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_health_db_check_overrides_get_db():
    from app.infrastructure.db import database

    app.dependency_overrides[database.get_db] = lambda: (MagicMock(),)

    res = client.get("/health/db")
    assert res.status_code == 200
    assert res.json() == {"status": "connected"}

    app.dependency_overrides.pop(database.get_db, None)
