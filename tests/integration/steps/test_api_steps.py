import json
from pytest_bdd import scenarios, given, when, then, parsers
import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from app.infrastructure.api.fastapi import app
from app.api import pedido as pedido_api
from app.api import status_pedido as status_api
from app.api import check as check_api
from tests.integration.conftest import FakePedido, FakeStatus


scenarios('../features')


@pytest.fixture(autouse=True)
def include_routers():
    # include routers once; safe to call multiple times in tests
    app.include_router(pedido_api.router)
    app.include_router(status_api.router)
    app.include_router(check_api.router)
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


@given('o gateway de pedidos retorna um pedido válido')
def given_pedido_gateway_returns_pedido():
    mock = MagicMock()
    mock.criar_pedido.return_value = FakePedido()
    return mock


@given('o gateway de pedido_produto retorna os produtos [1, 2]')
def given_pedido_prod_gateway_returns_produtos():
    mock = MagicMock()
    # Note: controllers expect buscarPorIdPedido to return list of objects with produto_id
    mock.buscarPorIdPedido.return_value = [MagicMock(produto_id=1), MagicMock(produto_id=2)]
    return mock


@given('o gateway de pedidos retorna uma lista de pedidos')
def given_pedido_gateway_list():
    mock = MagicMock()
    mock.listar_todos.return_value = [FakePedido(), FakePedido(id=2, cliente_id=43)]
    return mock


@given('o gateway de pedidos lança ValueError ao buscar por id')
def given_pedido_gateway_raises_on_search():
    mock = MagicMock()
    mock.buscar_por_id.side_effect = ValueError('Pedido não encontrado')
    return mock


@given('o gateway de status retorna um status válido')
def given_status_gateway_returns_status():
    mock = MagicMock()
    mock.criar.return_value = FakeStatus()
    return mock


@given('o gateway de status lança ValueError ao buscar por id')
def given_status_gateway_raises_on_search():
    mock = MagicMock()
    mock.buscar_por_id.side_effect = ValueError('Status não encontrado')
    return mock


@given('eu sobrescrevo dependência get_db')
def given_override_get_db():
    from app.infrastructure.db import database
    app.dependency_overrides[database.get_db] = lambda: (MagicMock(),)


@when(parsers.parse('eu envio um POST para "{path}" com o payload'), target_fixture='response')
def when_post_with_payload(client, path, request, given_pedido_gateway_returns_pedido, given_pedido_prod_gateway_returns_produtos):
    # set overrides if given fixtures exist
    if given_pedido_gateway_returns_pedido:
        app.dependency_overrides[pedido_api.get_pedido_gateway] = lambda: given_pedido_gateway_returns_pedido
    if given_pedido_prod_gateway_returns_produtos:
        app.dependency_overrides[pedido_api.get_pedido_produto_gateway] = lambda: given_pedido_prod_gateway_returns_produtos

    # simple default payload used by features
    payload = {"cliente_id": 42, "produtos": [1, 2]}
    return client.post(path, json=payload)


@when(parsers.parse('eu executo GET em "{path}"'), target_fixture='response_get')
def when_get(client, path):
    return client.get(path)


@then(parsers.parse('o status da resposta deve ser {status_code:d}'))
def then_status_code(response, status_code):
    assert response.status_code == status_code


@then(parsers.parse('o campo "{json_field}" do JSON deve ser "{value}"'))
def then_json_field_equals(response, json_field, value):
    data = response.json()
    parts = json_field.split('.')
    cur = data
    for p in parts:
        cur = cur.get(p)
    assert cur == value


@then(parsers.parse('o campo "{json_field}" do JSON deve ser {expected}'))
def then_json_field_equals_list(response, json_field, expected):
    data = response.json()
    parts = json_field.split('.')
    cur = data
    for p in parts:
        cur = cur.get(p)
    exp = json.loads(expected)
    assert cur == exp


@then(parsers.parse('o campo "{json_field}" do JSON deve estar em ({options})'))
def then_json_field_in_options(response, json_field, options):
    data = response.json()
    parts = json_field.split('.')
    cur = data
    for p in parts:
        cur = cur.get(p)
    opts = [o.strip().strip('"') for o in options.split(',')]
    assert cur in opts


@then(parsers.parse('o corpo JSON deve conter {expected}'))
def then_json_contains(response_get, expected):
    data = response_get.json()
    exp = json.loads(expected.replace("'", '"'))
    for k, v in exp.items():
        assert data.get(k) == v
