import os

import boto3
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# -------------------------------------------------
# Load .env
# -------------------------------------------------
env_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    ".env"
)

load_dotenv(env_path)


# -------------------------------------------------
# Configuration
# -------------------------------------------------
class Config:

    def __init__(self):
        self.db_host = os.getenv("host")
        self.db_port = int(os.getenv("port", "5432"))
        self.db_user = os.getenv("pg_user")
        self.db_name = os.getenv("pg_database")
        self.aws_region = os.getenv("aws_region", "us-east-1")

        print(
            f"Database configuration: "
            f"host={self.db_host}, "
            f"port={self.db_port}, "
            f"user={self.db_user}, "
            f"dbname={self.db_name}, "
            f"aws_region={self.aws_region}"
        )

        if not all([
            self.db_host,
            self.db_user,
            self.db_name,
            self.aws_region
        ]):
            raise ValueError(
                "Database configuration missing in .env file"
            )

    # -------------------------------------------------
    # Generate fresh AWS RDS IAM token
    # -------------------------------------------------
    def generate_iam_token(self):

        rds_client = boto3.client(
            "rds",
            region_name=self.aws_region
        )

        token = rds_client.generate_db_auth_token(
            DBHostname=self.db_host,
            Port=self.db_port,
            DBUsername=self.db_user,
            Region=self.aws_region
        )

        return token

    # -------------------------------------------------
    # SQLAlchemy URL
    # Password deliberately NOT included
    # -------------------------------------------------
    def get_database_connection_string(self):

        return URL.create(
            drivername="postgresql+psycopg",
            username=self.db_user,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            query={
                "sslmode": "require"
            }
        )

    # -------------------------------------------------
    # JDBC URL
    # -------------------------------------------------
    def get_jdbc_connection_string(self):

        return (
            f"jdbc:postgresql://"
            f"{self.db_host}:"
            f"{self.db_port}/"
            f"{self.db_name}"
            f"?sslmode=require"
        )

    # -------------------------------------------------
    # JDBC properties
    # Generates IAM token when called
    # -------------------------------------------------
    def get_db_connection_params(self):

        return {
            "user": self.db_user,
            "password": self.generate_iam_token(),
            "driver": "org.postgresql.Driver"
        }


# -------------------------------------------------
# Config Instance
# -------------------------------------------------
config = Config()


# -------------------------------------------------
# Database URL
# -------------------------------------------------
DATABASE_URL = config.get_database_connection_string()


# -------------------------------------------------
# SQLAlchemy Engine
# -------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False
)


# -------------------------------------------------
# IMPORTANT
# Generate fresh IAM token for every new
# physical database connection
# -------------------------------------------------
@event.listens_for(engine, "do_connect")
def provide_iam_token(
    dialect,
    conn_rec,
    cargs,
    cparams
):
    cparams["password"] = config.generate_iam_token()


# -------------------------------------------------
# Session Factory
# -------------------------------------------------
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


# -------------------------------------------------
# SQLAlchemy Base
# -------------------------------------------------
class Base(DeclarativeBase):
    pass


# -------------------------------------------------
# FastAPI Database Dependency
# -------------------------------------------------
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()