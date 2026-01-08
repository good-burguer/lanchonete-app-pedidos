import os
import json
from functools import lru_cache

import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

@lru_cache(maxsize=1)
def _get_database_url() -> str:
    env_url = os.getenv("DATABASE_URL", "").strip()

    if env_url:
        return env_url
    secret_name = os.getenv("DB_SECRET_NAME", "").strip()

    if not secret_name:
        raise RuntimeError(
            "DATABASE_URL not set and DB_SECRET_NAME is missing. "
            "Set DATABASE_URL for local dev or DB_SECRET_NAME for AWS."
        )
    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    sm = boto3.client("secretsmanager", region_name=region)
    secret = json.loads(sm.get_secret_value(SecretId=secret_name)["SecretString"])

    host = secret["host"]
    dbname = secret["dbname"]
    username = secret["username"]
    password = secret["password"]
    port = secret.get("port", 5432)

    return f"postgresql://{username}:{password}@{host}:{port}/{dbname}"

engine = create_engine(_get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()