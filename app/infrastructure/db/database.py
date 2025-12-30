from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("postgresql://gb_admin:#f3W^kLP}^4;!mF+?NL&W)w9@http://gb-dev-postgres.c6nea8wsy9hd.us-east-1.rds.amazonaws.com:5432/goodburger")
#engine = create_engine("postgresql://postgres:postgres@database_order:5432/lanchonete_pedido")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()