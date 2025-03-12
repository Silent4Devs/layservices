from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import settings  
from .ConnectionManager import ConnectionManager

Base = declarative_base()

class PostgreSQLManager(ConnectionManager):
    def __init__(self):
        """
        Open a PostgreSQL connection and initialize a session.
        """

        db_username = settings.DB_USERNAME
        db_password = settings.DB_PASSWORD
        db_host = settings.DB_HOST
        db_port = settings.DB_PORT
        db_database = settings.DB_DATABASE

        postgres_url = f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"

        self.engine = create_engine(postgres_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_client(self):
        """
        Returns a SQLAlchemy session.

        """
        return self.SessionLocal()

    def close_connection(self):
        """
        Close the PostgreSQL connection.
        """
        self.engine.dispose()
        print("PostgreSQL connection closed.")