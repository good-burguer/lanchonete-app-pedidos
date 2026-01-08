"""Unit tests for DAO classes"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy.exc import IntegrityError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.dao.pedido_dao import PedidoDAO
from app.dao.pedido_produto_dao import PedidoProdutoDAO
from app.dao.status_pedido_dao import StatusPedidoDAO
from app.entities.pedido.entities import Pedido
from app.models.pedido_produto import PedidoProdutoModel
from app.models.status_pedido import StatusPedido


class TestPedidoDAO:
    """Tests for PedidoDAO"""
    
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock()
    
    @pytest.fixture
    def dao(self, mock_db_session):
        return PedidoDAO(mock_db_session)
    
    def test_criar_pedido_success(self, dao, mock_db_session):
        """Test successfully creating a pedido"""
        pedido = MagicMock()
        pedido.cliente_id = 1
        
        result = dao.criar_pedido(pedido)
        
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_db_session.refresh.assert_called_once()
    
    def test_criar_pedido_integrity_error(self, dao, mock_db_session):
        """Test crear_pedido with IntegrityError"""
        mock_db_session.add.side_effect = IntegrityError("Duplicate", "orig", "params")
        
        pedido = MagicMock()
        pedido.cliente_id = 1
        
        with pytest.raises(Exception) as exc_info:
            dao.criar_pedido(pedido)
        
        assert "Erro de integridade" in str(exc_info.value)
        mock_db_session.rollback.assert_called_once()
    
    def test_busca_por_status(self, dao, mock_db_session):
        """Test searching pedidos by status"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.all.return_value = []
        
        result = dao.busca_por_status("1")
        
        assert result == []
    
    def test_buscar_por_id(self, dao, mock_db_session):
        """Test fetching pedido by id"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = MagicMock(id=1)
        
        result = dao.buscar_por_id(1)
        
        assert result.id == 1
    
    def test_buscar_por_id_not_found(self, dao, mock_db_session):
        """Test fetching non-existent pedido"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        result = dao.buscar_por_id(999)
        
        assert result is None
    
    def test_atualizar_pedido(self, dao, mock_db_session):
        """Test updating a pedido"""
        mock_entity = MagicMock()
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_entity
        
        pedido_request = MagicMock()
        pedido_request.status = "2"
        pedido_request.model_dump.return_value = {"status": "2"}
        
        result = dao.atualizar_pedido(1, pedido_request)
        
        mock_db_session.commit.assert_called()
        mock_db_session.refresh.assert_called()
    
    def test_atualizar_pedido_not_found(self, dao, mock_db_session):
        """Test updating non-existent pedido"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        pedido_request = MagicMock()
        pedido_request.status = "2"
        
        result = dao.atualizar_pedido(999, pedido_request)
        
        assert result is None
    
    def test_deletar_pedido_success(self, dao, mock_db_session):
        """Test successfully deleting a pedido"""
        mock_entity = MagicMock()
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_entity
        
        dao.deletar_pedido(1)
        
        mock_db_session.delete.assert_called_once()
        mock_db_session.commit.assert_called_once()
    
    def test_deletar_pedido_not_found(self, dao, mock_db_session):
        """Test deleting non-existent pedido"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        with pytest.raises(ValueError) as exc_info:
            dao.deletar_pedido(999)
        
        assert "Pedido não encontrado" in str(exc_info.value)


class TestPedidoProdutoDAO:
    """Tests for PedidoProdutoDAO"""
    
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock()
    
    @pytest.fixture
    def dao(self, mock_db_session):
        return PedidoProdutoDAO(mock_db_session)
    
    def test_criar_pedido_produto_success(self, dao, mock_db_session):
        """Test successfully creating a pedido produto"""
        result = dao.criar_pedido_produto(1, 2)
        
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
    
    def test_criar_pedido_produto_integrity_error(self, dao, mock_db_session):
        """Test criar_pedido_produto with IntegrityError"""
        mock_db_session.add.side_effect = IntegrityError("Duplicate", "orig", "params")
        
        with pytest.raises(Exception) as exc_info:
            dao.criar_pedido_produto(1, 2)
        
        assert "Erro de integridade" in str(exc_info.value)
        mock_db_session.rollback.assert_called_once()
    
    def test_buscar_por_id_pedido(self, dao, mock_db_session):
        """Test searching pedido produtos by pedido_id"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.all.return_value = [MagicMock(id=1), MagicMock(id=2)]
        
        result = dao.buscarPorIdPedido(1)
        
        assert len(result) == 2
    
    def test_deletar_existe(self, dao, mock_db_session):
        """Test deleting an existing pedido produto"""
        mock_entity = MagicMock()
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = mock_entity
        
        dao.deletar(1)
        
        mock_db_session.delete.assert_called_once()
        mock_db_session.commit.assert_called_once()
    
    def test_deletar_nao_existe(self, dao, mock_db_session):
        """Test deleting non-existent pedido produto"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.first.return_value = None
        
        dao.deletar(999)
        
        mock_db_session.delete.assert_not_called()


class TestStatusPedidoDAO:
    """Tests for StatusPedidoDAO"""
    
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock()
    
    @pytest.fixture
    def dao(self, mock_db_session):
        return StatusPedidoDAO(mock_db_session)
    
    def test_criar_success(self, dao, mock_db_session):
        """Test successfully creating a status"""
        status = MagicMock()
        status.descricao = "Novo Status"
        
        result = dao.criar(status)
        
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
    
    def test_criar_integrity_error(self, dao, mock_db_session):
        """Test criar with IntegrityError"""
        mock_db_session.add.side_effect = IntegrityError("Duplicate", "orig", "params")
        
        status = MagicMock()
        status.descricao = "Novo Status"
        
        with pytest.raises(Exception) as exc_info:
            dao.criar(status)
        
        assert "Erro de integridade" in str(exc_info.value)
    
    def test_buscar_por_id_success(self, dao, mock_db_session):
        """Test fetching status by id"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.first.return_value = MagicMock(id=1, descricao="Pronto")
        
        result = dao.buscar_por_id(1)
        
        assert result.id == 1
    
    def test_buscar_por_id_not_found(self, dao, mock_db_session):
        """Test fetching non-existent status"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.first.return_value = None
        
        result = dao.buscar_por_id(999)
        
        assert result is None
    
    def test_listar_todos(self, dao, mock_db_session):
        """Test listing all statuses"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.all.return_value = [MagicMock(id=1), MagicMock(id=2)]
        
        result = dao.listar_todos()
        
        assert len(result) == 2
    
    def test_atualizar_success(self, dao, mock_db_session):
        """Test updating a status"""
        mock_entity = MagicMock()
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.first.return_value = mock_entity
        
        status = MagicMock()
        status.descricao = "Atualizado"
        status.model_dump.return_value = {"descricao": "Atualizado"}
        
        result = dao.atualizar(1, status)
        
        mock_db_session.commit.assert_called()
        mock_db_session.refresh.assert_called()
    
    def test_atualizar_not_found(self, dao, mock_db_session):
        """Test updating non-existent status"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.first.return_value = None
        
        status = MagicMock()
        status.descricao = "Atualizado"
        
        result = dao.atualizar(999, status)
        
        assert result is None
    
    def test_deletar_success(self, dao, mock_db_session):
        """Test deleting a status"""
        mock_entity = MagicMock()
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.first.return_value = mock_entity
        
        dao.deletar(1)
        
        mock_db_session.delete.assert_called_once()
        mock_db_session.commit.assert_called_once()
    
    def test_deletar_not_found(self, dao, mock_db_session):
        """Test deleting non-existent status"""
        mock_query = MagicMock()
        mock_db_session.query.return_value = mock_query
        mock_query.filter_by.return_value = mock_query
        mock_query.first.return_value = None
        
        dao.deletar(999)
        
        mock_db_session.delete.assert_not_called()
