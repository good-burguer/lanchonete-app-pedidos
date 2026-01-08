"""Extended unit tests for PedidoController"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.controllers.pedido_controller import PedidoController
from app.adapters.dto.pedido_dto import PedidoAtualizaSchema


@pytest.fixture
def mock_db_session():
    """Mock database session"""
    return MagicMock()


@pytest.fixture
def mock_pedido_gateway():
    """Mock pedido gateway"""
    return MagicMock()


@pytest.fixture
def mock_pedido_produto_gateway():
    """Mock pedido produto gateway"""
    return MagicMock()


@pytest.fixture
def controller(mock_db_session):
    """Create a controller instance"""
    return PedidoController(db_session=mock_db_session)


class TestPedidoControllerCreate:
    """Tests for criar_pedido method"""
    
    def test_criar_pedido_raises_exception_on_error(self, controller, mock_pedido_gateway, mock_pedido_produto_gateway):
        """Test that criar_pedido raises HTTPException on error"""
        mock_pedido_gateway.criar_pedido.side_effect = Exception("Database error")

        pedido = MagicMock()
        pedido.cliente_id = 1
        pedido.produtos = [1, 2]

        with pytest.raises(HTTPException) as exc_info:
            controller.criar_pedido(pedido, mock_pedido_produto_gateway)
        
        assert exc_info.value.status_code == 400


class TestPedidoControllerList:
    """Tests for listar_todos method"""
    
    def test_listar_todos_returns_response(self, controller, mock_db_session):
        """Test that listar_todos returns a response"""
        mock_pedido = MagicMock()
        mock_pedido.id = 1
        mock_pedido.cliente_id = 5
        mock_pedido.status_rel = MagicMock(id=2, descricao="Em preparo")
        mock_pedido.data_criacao = None
        mock_pedido.data_alteracao = None
        mock_pedido.data_finalizacao = None
        
        mock_db_session.listar_todos.return_value = [mock_pedido]

        response = controller.listar_todos()

        assert response.status == "sucess"  # Note: there's a typo in the original code
        assert len(response.data) == 1


class TestPedidoControllerGetById:
    """Tests for buscar_por_id method"""
    
    def test_buscar_por_id_with_value_error(self, controller, mock_db_session, mock_pedido_produto_gateway):
        """Test buscar_por_id raises HTTPException on ValueError"""
        mock_db_session.buscar_por_id.side_effect = ValueError("Pedido não encontrado")

        with pytest.raises(HTTPException) as exc_info:
            controller.buscar_por_id(999, mock_pedido_produto_gateway)
        
        assert exc_info.value.status_code == 404

    def test_buscar_por_id_with_general_exception(self, controller, mock_db_session, mock_pedido_produto_gateway):
        """Test buscar_por_id raises HTTPException on general Exception"""
        mock_db_session.buscar_por_id.side_effect = Exception("Database error")

        with pytest.raises(HTTPException) as exc_info:
            controller.buscar_por_id(1, mock_pedido_produto_gateway)
        
        assert exc_info.value.status_code == 400


class TestPedidoControllerUpdate:
    """Tests for atualizar_pedido method"""
    
    def test_atualizar_pedido_with_value_error(self, controller, mock_db_session, mock_pedido_produto_gateway):
        """Test atualizar_pedido raises HTTPException on ValueError"""
        mock_db_session.atualizar_pedido.side_effect = ValueError("Pedido não encontrado")

        update_schema = PedidoAtualizaSchema(status="2")

        with pytest.raises(HTTPException) as exc_info:
            controller.atualizar_pedido(999, update_schema, mock_pedido_produto_gateway)
        
        assert exc_info.value.status_code == 404

    def test_atualizar_pedido_with_general_exception(self, controller, mock_db_session, mock_pedido_produto_gateway):
        """Test atualizar_pedido raises HTTPException on general Exception"""
        mock_db_session.atualizar_pedido.side_effect = Exception("Database error")

        update_schema = PedidoAtualizaSchema(status="2")

        with pytest.raises(HTTPException) as exc_info:
            controller.atualizar_pedido(1, update_schema, mock_pedido_produto_gateway)
        
        assert exc_info.value.status_code == 400


class TestPedidoControllerDelete:
    """Tests for deletar method"""
    
    def test_deletar_with_value_error(self, controller, mock_db_session, mock_pedido_produto_gateway):
        """Test deletar raises HTTPException on ValueError"""
        mock_db_session.deletar_pedido.side_effect = ValueError("Pedido não encontrado")

        with pytest.raises(HTTPException) as exc_info:
            controller.deletar(999, mock_pedido_produto_gateway)
        
        assert exc_info.value.status_code == 404

    def test_deletar_with_general_exception(self, controller, mock_db_session, mock_pedido_produto_gateway):
        """Test deletar raises HTTPException on general Exception"""
        mock_db_session.deletar_pedido.side_effect = Exception("Database error")

        with pytest.raises(HTTPException) as exc_info:
            controller.deletar(1, mock_pedido_produto_gateway)
        
        assert exc_info.value.status_code == 400

    def test_deletar_success(self, controller, mock_db_session, mock_pedido_produto_gateway):
        """Test successful deletion returns 204 response"""
        response = controller.deletar(1, mock_pedido_produto_gateway)

        assert response.status_code == 204
