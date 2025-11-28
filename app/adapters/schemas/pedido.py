from pydantic import BaseModel, EmailStr, constr, ConfigDict

import datetime
from typing import Optional
from typing import List

from app.adapters.schemas.status_pedido import StatusPedidoResponseSchema
from app.adapters.schemas.pedido_produto import PedidoProdutoResponseSchema

class PedidoResponseSchema(BaseModel):
    id: int
    cliente_id: int
    status: StatusPedidoResponseSchema
    data_criacao: datetime.time
    data_alteracao: Optional[datetime.time]
    data_finalizacao: Optional[datetime.time]
    
    class Config:
        allow_population_by_field_name = True
    
class PedidoProdutosResponseSchema(BaseModel):
    id: int
    cliente_id: int
    status: StatusPedidoResponseSchema
    data_criacao: datetime.time
    data_alteracao: Optional[datetime.time]
    data_finalizacao: Optional[datetime.time]
    produtos: List[int]
    
    class Config:
        allow_population_by_field_name = True

