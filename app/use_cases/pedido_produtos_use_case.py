from app.entities.pedido_produto.entities import PedidoProdutoEntities
from app.models.pedido_produto import PedidoProdutoModel
from app.adapters.schemas.pedido_produto import ProdutoPedidoResponseSchema

from app.adapters.utils.debug import var_dump_die

class PedidoProdutosUseCase:
    def __init__(self, pedido_produtos_gateway: PedidoProdutoEntities):
        self.pedido_produtos_gateway = pedido_produtos_gateway

    def criarPedidoProdutos(self, pedido_id: int, produtos: list) -> ProdutoPedidoResponseSchema:
        if isinstance(produtos, list):
            produtosCriados = [];
            
            for produto in produtos:
                produtosCriados.append(
                    (self._criarPedidoProduto(
                        pedido_id=pedido_id, 
                        produto_id=produto)))

        return self.buscarPorIdPedido(pedido_id=pedido_id)
    
    def _criarPedidoProduto(self, pedido_id: int, produto_id: list): 
        self.pedido_produtos_gateway.criarPedidoProduto(pedido_id=pedido_id, produto_id=produto_id)
        
    
    def buscarPorIdPedido(self, pedido_id: int) -> ProdutoPedidoResponseSchema:
        product_orders = self.pedido_produtos_gateway.buscarPorIdPedido(pedido_id=pedido_id)
        items = []
        
        for item in product_orders:
            items.append(item.produto_id)

        return items
    
    def deletarPorPedido(self, pedido_id: int) -> None:
        pedidoProdutos: PedidoProdutoModel = self.pedido_produtos_gateway.buscarPorIdPedido(pedido_id=pedido_id)
        
        if pedidoProdutos:
            for pedidoProduto in pedidoProdutos:
                self.pedido_produtos_gateway.deletar(id=pedidoProduto.id)