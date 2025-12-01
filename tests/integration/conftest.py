import sys, os
from pathlib import Path
import pytest
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


class FakePedido:
    def __init__(self, id=1, cliente_id=42):
        self.id = id
        self.cliente_id = cliente_id
        class S:
            pass
        self.status_rel = S()
        self.status_rel.id = 2
        self.status_rel.descricao = "Em preparo"
        self.data_criacao = datetime.time(12, 0, 0)
        self.data_alteracao = None
        self.data_finalizacao = None


class FakeStatus:
    def __init__(self, id=1, descricao="Pronto"):
        self.id = id
        self.descricao = descricao


@pytest.fixture
def fake_pedido():
    return FakePedido()


@pytest.fixture
def fake_status():
    return FakeStatus()