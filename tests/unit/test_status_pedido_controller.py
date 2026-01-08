"""Extended unit tests for StatusPedidoController"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.controllers.status_pedido_controller import StatusPedidoController
from app.adapters.dto.status_pedido_dto import StatusPedidoUpdateSchema


@pytest.fixture
def mock_db_session():
    """Mock database session"""
    return MagicMock()


@pytest.fixture
def controller(mock_db_session):
    """Create a controller instance"""
    return StatusPedidoController(db_session=mock_db_session)


class TestStatusPedidoControllerCreate:
    """Tests for criar method"""
    
    def test_criar_with_error(self, controller, mock_db_session):
        """Test criar raises HTTPException on error"""
        mock_db_session.criar.side_effect = Exception("Database error")

        data = MagicMock()
        data.descricao = "Novo Status"

        with pytest.raises(HTTPException) as exc_info:
            controller.criar(data)
        
        assert exc_info.value.status_code == 400

    def test_criar_success(self, controller, mock_db_session):
        """Test criar returns success response"""
        mock_status = MagicMock()
        mock_status.id = 1
        mock_status.descricao = "Pronto"
        
        mock_db_session.criar.return_value = mock_status

        data = MagicMock()
        data.descricao = "Novo Status"

        response = controller.criar(data)

        assert response.status == "success"
        assert response.data.id == 1


class TestStatusPedidoControllerGetById:
    """Tests for buscar_por_id method"""
    
    def test_buscar_por_id_not_found(self, controller, mock_db_session):
        """Test buscar_por_id raises HTTPException with 404 on ValueError"""
        mock_db_session.buscar_por_id.side_effect = ValueError("Status não encontrado")

        with pytest.raises(HTTPException) as exc_info:
            controller.buscar_por_id(999)
        
        assert exc_info.value.status_code == 404

    def test_buscar_por_id_with_error(self, controller, mock_db_session):
        """Test buscar_por_id raises HTTPException with 400 on general error"""
        mock_db_session.buscar_por_id.side_effect = Exception("Database error")

        with pytest.raises(HTTPException) as exc_info:
            controller.buscar_por_id(1)
        
        assert exc_info.value.status_code == 400

    def test_buscar_por_id_success(self, controller, mock_db_session):
        """Test buscar_por_id returns success response"""
        mock_status = MagicMock()
        mock_status.id = 1
        mock_status.descricao = "Pronto"
        
        mock_db_session.buscar_por_id.return_value = mock_status

        response = controller.buscar_por_id(1)

        assert response.status == "success"
        assert response.data.id == 1


class TestStatusPedidoControllerList:
    """Tests for listar_todos method"""
    
    def test_listar_todos_with_error(self, controller, mock_db_session):
        """Test listar_todos raises HTTPException on error"""
        mock_db_session.listar_todos.side_effect = Exception("Database error")

        with pytest.raises(HTTPException) as exc_info:
            controller.listar_todos()
        
        assert exc_info.value.status_code == 400

    def test_listar_todos_success(self, controller, mock_db_session):
        """Test listar_todos returns success response"""
        mock_status = MagicMock()
        mock_status.id = 1
        mock_status.descricao = "Pronto"
        
        mock_db_session.listar_todos.return_value = [mock_status]

        response = controller.listar_todos()

        assert response.status == "success"
        assert len(response.data) == 1


class TestStatusPedidoControllerUpdate:
    """Tests for atualizar method"""
    
    def test_atualizar_not_found(self, controller, mock_db_session):
        """Test atualizar raises HTTPException with 404 on ValueError"""
        mock_db_session.atualizar.side_effect = ValueError("Status não encontrado")

        data = StatusPedidoUpdateSchema(descricao="Atualizado")

        with pytest.raises(HTTPException) as exc_info:
            controller.atualizar(999, data)
        
        assert exc_info.value.status_code == 404

    def test_atualizar_with_error(self, controller, mock_db_session):
        """Test atualizar raises HTTPException with 400 on general error"""
        mock_db_session.atualizar.side_effect = Exception("Database error")

        data = StatusPedidoUpdateSchema(descricao="Atualizado")

        with pytest.raises(HTTPException) as exc_info:
            controller.atualizar(1, data)
        
        assert exc_info.value.status_code == 400

    def test_atualizar_success(self, controller, mock_db_session):
        """Test atualizar returns success response"""
        mock_status = MagicMock()
        mock_status.id = 1
        mock_status.descricao = "Atualizado"
        
        mock_db_session.atualizar.return_value = mock_status

        data = StatusPedidoUpdateSchema(descricao="Atualizado")

        response = controller.atualizar(1, data)

        assert response.status == "success"
        assert response.data.descricao == "Atualizado"


class TestStatusPedidoControllerDelete:
    """Tests for deletar method"""
    
    def test_deletar_not_found(self, controller, mock_db_session):
        """Test deletar raises HTTPException with 404 on ValueError"""
        mock_db_session.deletar.side_effect = ValueError("Status não encontrado")

        with pytest.raises(HTTPException) as exc_info:
            controller.deletar(999)
        
        assert exc_info.value.status_code == 404

    def test_deletar_with_error(self, controller, mock_db_session):
        """Test deletar raises HTTPException with 400 on general error"""
        mock_db_session.deletar.side_effect = Exception("Database error")

        with pytest.raises(HTTPException) as exc_info:
            controller.deletar(1)
        
        assert exc_info.value.status_code == 400

    def test_deletar_success(self, controller, mock_db_session):
        """Test deletar returns 204 response"""
        response = controller.deletar(1)

        assert response.status_code == 204
