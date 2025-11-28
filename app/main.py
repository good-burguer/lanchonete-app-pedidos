from app.infrastructure.api.fastapi import app

from app.api import check
from app.api import pedido
from app.api import status_pedido

app.include_router(check.router)
app.include_router(pedido.router)
app.include_router(status_pedido.router)
