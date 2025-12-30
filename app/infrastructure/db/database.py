import os
import json
from functools import lru_cache

import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

@lru_cache(maxsize=1)
def _get_database_url() -> str:
    """
    Resolve the database URL using the following precedence:
    1) DATABASE_URL env var (local/dev override)
    2) AWS Secrets Manager via DB_SECRET_NAME (recommended for EKS with IRSA)

    The secret is expected to be a JSON with keys:
    host, dbname, username, password (and optionally port).
    """
    # 1) Local/dev override
    env_url = os.getenv("DATABASE_URL", "").strip()
    if env_url:
        return env_url

    # 2) Secrets Manager (prod)
    secret_name = os.getenv("DB_SECRET_NAME", "").strip()
    if not secret_name:
        raise RuntimeError(
            "DATABASE_URL not set and DB_SECRET_NAME is missing. "
            "Set DATABASE_URL for local dev or DB_SECRET_NAME for AWS."
        )

    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    sm = boto3.client("secretsmanager", region_name=region)
    secret = json.loads(sm.get_secret_value(SecretId=secret_name)["SecretString"])

    # host = secret["host"]
    # dbname = secret["dbname"]
    # username = secret["username"]
    # password = secret["password"]

    host = "gb-dev-postgres.c6nea8wsy9hd.us-east-1.rds.amazonaws.com"
    dbname = "goodburger"
    username = "gb_admin"
    password = "#f3W^kLP}^4;!mF+?NL&W)w9"
    port = secret.get("port", 5432)

    return f"postgresql://{username}:{password}@{host}:{port}/{dbname}"


# Create engine once per process
engine = create_engine(_get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()