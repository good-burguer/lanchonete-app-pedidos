from pydantic import BaseModel, ConfigDict

class PedidoProdutoCreateSchema(BaseModel):
    pedido_id: int
    produto_id: int

class PedidoProdutoResponseSchema(PedidoProdutoCreateSchema):
    pedido_id: int
    produto_id: int

    model_config = ConfigDict(validate_by_name=True)
    
class ProdutoPedidoResponseSchema(BaseModel):
    produto_id: int

    model_config = ConfigDict(validate_by_name=True)