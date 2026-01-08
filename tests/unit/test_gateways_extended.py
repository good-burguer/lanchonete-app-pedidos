"""Extended unit tests for gateway classes"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.gateways.pedido_gateway import PedidoGateway
from app.gateways.status_pedido_gateway import StatusPedidoGateway
from app.gateways.pedido_produto_gateway import PedidoProdutoGateway


class TestPedidoGateway:
    """Tests for PedidoGateway"""
    
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock()
    
    @pytest.fixture
    def gateway(self, mock_db_session):
        return PedidoGateway(db_session=mock_db_session)
    
    def test_criar_pedido(self, gateway):
        """Test criar_pedido delegates to DAO"""
        pedido = MagicMock()
        pedido.cliente_id = 1
        
        gateway.criar_pedido(pedido)
        
        gateway.dao.criar_pedido.assert_called_once_with(pedido)
    
    def test_listar_todos(self, gateway):
        """Test listar_todos calls DAO with multiple statuses"""
        mock_pedido1 = MagicMock(id=1)
        mock_pedido2 = MagicMock(id=2)
        mock_pedido3 = MagicMock(id=3)
        
        gateway.dao.busca_por_status = MagicMock(side_effect=[
            [mock_pedido3],  # Status 3 (Pronto)
            [mock_pedido2],  # Status 2 (Em preparação)
            [mock_pedido1]   # Status 1 (Recebido)
        ])
        
        result = gateway.listar_todos()
        
        assert len(result) == 3
        assert gateway.dao.busca_por_status.call_count == 3
    
    def test_buscar_por_id(self, gateway):
        """Test buscar_por_id delegates to DAO"""
        gateway.buscar_por_id(1)
        
        gateway.dao.buscar_por_id.assert_called_once_with(1)
    
    def test_atualizar_pedido(self, gateway):
        """Test atualizar_pedido delegates to DAO"""
        pedido_request = MagicMock()
        
        gateway.atualizar_pedido(1, pedido_request)
        
        gateway.dao.atualizar_pedido.assert_called_once_with(1, pedido_request)
    
    def test_deletar_pedido(self, gateway):
        """Test deletar_pedido delegates to DAO"""
        gateway.deletar_pedido(1)
        
        gateway.dao.deletar_pedido.assert_called_once_with(1)


class TestStatusPedidoGateway:
    """Tests for StatusPedidoGateway"""
    
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock()
    
    @pytest.fixture
    def gateway(self, mock_db_session):
        return StatusPedidoGateway(db_session=mock_db_session)
    
    def test_criar(self, gateway):
        """Test criar delegates to DAO"""
        status = MagicMock()
        status.descricao = "Novo Status"
        
        gateway.criar(status)
        
        gateway.dao.criar.assert_called_once_with(status)
    
    def test_buscar_por_id_found(self, gateway):
        """Test buscar_por_id returns status when found"""
        mock_status = MagicMock(id=1)
        gateway.dao.buscar_por_id = MagicMock(return_value=mock_status)
        
        result = gateway.buscar_por_id(1)
        
        assert result.id == 1
    
    def test_buscar_por_id_not_found(self, gateway):
        """Test buscar_por_id returns None when not found"""
        gateway.dao.buscar_por_id = MagicMock(return_value=None)
        
        result = gateway.buscar_por_id(999)
        
        assert result is None
    
    def test_listar_todos(self, gateway):
        """Test listar_todos delegates to DAO"""
        mock_statuses = [MagicMock(id=1), MagicMock(id=2)]
        gateway.dao.listar_todos = MagicMock(return_value=mock_statuses)
        
        result = gateway.listar_todos()
        
        assert len(result) == 2
    
    def test_atualizar(self, gateway):
        """Test atualizar delegates to DAO"""
        status = MagicMock()
        
        gateway.atualizar(1, status)
        
        gateway.dao.atualizar.assert_called_once_with(1, status)
    
    def test_deletar(self, gateway):
        """Test deletar delegates to DAO"""
        gateway.deletar(1)
        
        gateway.dao.deletar.assert_called_once_with(1)


class TestPedidoProdutoGateway:
    """Tests for PedidoProdutoGateway"""
    
    @pytest.fixture
    def mock_db_session(self):
        return MagicMock()
    
    @pytest.fixture
    def gateway(self, mock_db_session):
        return PedidoProdutoGateway(db_session=mock_db_session)
    
    def test_criar_pedido_produto(self, gateway):
        """Test criar_pedido_produto delegates to DAO"""
        gateway.criar_pedido_produto(1, 2)
        
        gateway.dao.criar_pedido_produto.assert_called_once_with(1, 2)
    
    def test_buscar_por_id_pedido(self, gateway):
        """Test buscarPorIdPedido delegates to DAO"""
        gateway.buscarPorIdPedido(1)
        
        gateway.dao.buscarPorIdPedido.assert_called_once_with(1)
    
    def test_deletar_por_pedido(self, gateway):
        """Test deletarPorPedido calls DAO for each produto"""
        mock_produto1 = MagicMock(id=1)
        mock_produto2 = MagicMock(id=2)
        gateway.dao.buscarPorIdPedido = MagicMock(return_value=[mock_produto1, mock_produto2])
        
        gateway.deletarPorPedido(1)
        
        assert gateway.dao.deletar.call_count == 2
