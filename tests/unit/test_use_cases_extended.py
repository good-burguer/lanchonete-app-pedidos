"""Extended unit tests for use cases"""

import sys
import os
from pathlib import Path
import pytest
from unittest.mock import MagicMock

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.use_cases.pedido_use_case import PedidoUseCase
from app.use_cases.status_pedido_use_case import StatusPedidoUseCase
from app.use_cases.pedido_produtos_use_case import PedidoProdutosUseCase
from app.adapters.dto.pedido_dto import PedidoAtualizaSchema
from app.adapters.dto.status_pedido_dto import StatusPedidoUpdateSchema


class TestPedidoUseCaseExtended:
    """Extended tests for PedidoUseCase"""
    
    @pytest.fixture
    def mock_entity(self):
        return MagicMock()
    
    @pytest.fixture
    def use_case(self, mock_entity):
        return PedidoUseCase(mock_entity)
    
    def test_buscar_por_id_found(self, use_case, mock_entity):
        """Test buscar_por_id when pedido is found"""
        fake_db_obj = MagicMock()
        fake_db_obj.id = 1
        fake_db_obj.cliente_id = 5
        fake_db_obj.status_rel = MagicMock()
        fake_db_obj.status_rel.id = 2
        fake_db_obj.status_rel.descricao = "Em preparo"
        fake_db_obj.data_criacao = None
        fake_db_obj.data_alteracao = None
        fake_db_obj.data_finalizacao = None
        
        mock_entity.buscar_por_id.return_value = fake_db_obj
        
        response = use_case.buscar_por_id(1)
        
        assert response.id == fake_db_obj.id
    
    def test_deletar_pedido(self, use_case, mock_entity):
        """Test deletar_pedido method"""
        use_case.deletar_pedido(1)
        
        mock_entity.deletar_pedido.assert_called_once_with(1)
    
    def test_atualizar_pedido_success(self, use_case, mock_entity):
        """Test atualizar_pedido successfully"""
        fake_db_obj = MagicMock()
        fake_db_obj.id = 1
        fake_db_obj.cliente_id = 5
        fake_db_obj.status_rel = MagicMock()
        fake_db_obj.status_rel.id = 2
        fake_db_obj.status_rel.descricao = "Em preparo"
        fake_db_obj.data_criacao = None
        fake_db_obj.data_alteracao = None
        fake_db_obj.data_finalizacao = None
        
        mock_entity.atualizar_pedido.return_value = fake_db_obj
        
        update_request = PedidoAtualizaSchema(status="2")
        response = use_case.atualizar_pedido(1, update_request)
        
        assert response.id == 1
    
    def test_atualizar_pedido_not_found(self, use_case, mock_entity):
        """Test atualizar_pedido raises when not found"""
        mock_entity.atualizar_pedido.return_value = None
        
        update_request = PedidoAtualizaSchema(status="2")
        
        with pytest.raises(ValueError) as exc_info:
            use_case.atualizar_pedido(999, update_request)
        
        assert "Pedido não encontrado" in str(exc_info.value)


class TestStatusPedidoUseCaseExtended:
    """Extended tests for StatusPedidoUseCase"""
    
    @pytest.fixture
    def mock_entity(self):
        return MagicMock()
    
    @pytest.fixture
    def use_case(self, mock_entity):
        return StatusPedidoUseCase(mock_entity)
    
    def test_criar_success(self, use_case, mock_entity):
        """Test criar returns success response"""
        mock_status = MagicMock()
        mock_status.id = 1
        mock_status.descricao = "Pronto"
        
        mock_entity.criar.return_value = mock_status
        
        from app.adapters.dto.status_pedido_dto import StatusPedidoCreateSchema
        request = StatusPedidoCreateSchema(descricao="Pronto")
        response = use_case.criar(request)
        
        assert response.id == 1
        assert response.descricao == "Pronto"
    
    def test_buscar_por_id_not_found(self, use_case, mock_entity):
        """Test buscar_por_id raises when not found"""
        mock_entity.buscar_por_id.return_value = None
        
        with pytest.raises(ValueError) as exc_info:
            use_case.buscar_por_id(999)
        
        assert "Status não encontrado" in str(exc_info.value)
    
    def test_listar_todos_empty(self, use_case, mock_entity):
        """Test listar_todos with empty list"""
        mock_entity.listar_todos.return_value = []
        
        response = use_case.listar_todos()
        
        assert response == []
    
    def test_listar_todos_with_items(self, use_case, mock_entity):
        """Test listar_todos with multiple items"""
        mock_status1 = MagicMock()
        mock_status1.id = 1
        mock_status1.descricao = "Status 1"
        
        mock_status2 = MagicMock()
        mock_status2.id = 2
        mock_status2.descricao = "Status 2"
        
        mock_entity.listar_todos.return_value = [mock_status1, mock_status2]
        
        response = use_case.listar_todos()
        
        assert len(response) == 2
    
    def test_atualizar_success(self, use_case, mock_entity):
        """Test atualizar successfully"""
        mock_status = MagicMock()
        mock_status.id = 1
        mock_status.descricao = "Atualizado"
        
        mock_entity.buscar_por_id.return_value = mock_status
        mock_entity.atualizar.return_value = mock_status
        
        data = StatusPedidoUpdateSchema(descricao="Atualizado")
        response = use_case.atualizar(1, data)
        
        assert response.id == 1
        assert response.descricao == "Atualizado"
    
    def test_atualizar_not_found(self, use_case, mock_entity):
        """Test atualizar raises when not found"""
        mock_entity.buscar_por_id.return_value = None
        
        data = StatusPedidoUpdateSchema(descricao="Atualizado")
        
        with pytest.raises(ValueError) as exc_info:
            use_case.atualizar(999, data)
        
        assert "Status não encontrado" in str(exc_info.value)
    
    def test_deletar(self, use_case, mock_entity):
        """Test deletar method"""
        use_case.deletar(1)
        
        mock_entity.deletar.assert_called_once_with(id=1)


class TestPedidoProdutosUseCaseExtended:
    """Extended tests for PedidoProdutosUseCase"""
    
    @pytest.fixture
    def mock_gateway(self):
        return MagicMock()
    
    @pytest.fixture
    def use_case(self, mock_gateway):
        return PedidoProdutosUseCase(mock_gateway)
    
    def test_criar_pedido_produtos_success(self, use_case, mock_gateway):
        """Test criarPedidoProdutos successfully"""
        mock_produto1 = MagicMock(id=1)
        mock_produto2 = MagicMock(id=2)
        
        mock_gateway.criar_pedido_produto.side_effect = [mock_produto1, mock_produto2]
        
        response = use_case.criarPedidoProdutos(1, [1, 2])
        
        assert len(response) == 2
        assert mock_gateway.criar_pedido_produto.call_count == 2
    
    def test_buscar_por_id_pedido(self, use_case, mock_gateway):
        """Test buscarPorIdPedido"""
        mock_produtos = [MagicMock(produto_id=1), MagicMock(produto_id=2)]
        mock_gateway.buscarPorIdPedido.return_value = mock_produtos
        
        response = use_case.buscarPorIdPedido(1)
        
        assert len(response) == 2
    
    def test_deletar_por_pedido_success(self, use_case, mock_gateway):
        """Test deletarPorPedido successfully"""
        mock_produto1 = MagicMock(id=1)
        mock_produto2 = MagicMock(id=2)
        
        mock_gateway.buscarPorIdPedido.return_value = [mock_produto1, mock_produto2]
        
        use_case.deletarPorPedido(1)
        
        assert mock_gateway.deletar.call_count == 2
    
    def test_deletar_por_pedido_empty(self, use_case, mock_gateway):
        """Test deletarPorPedido with no products"""
        mock_gateway.buscarPorIdPedido.return_value = []
        
        use_case.deletarPorPedido(1)
        
        mock_gateway.deletar.assert_not_called()
