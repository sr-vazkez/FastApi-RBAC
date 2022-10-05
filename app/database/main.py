from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

#SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{config('DATABASE_USER')}:{config('DATABASE_PASSWORD')}@{config('DATABASE_HOSTNAME')}:{config('DATABASE_PORT')}/{config('DATABASE_NAME')}"
SQLALCHEMY_DATABASE_URL = "sqlite:///database.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, pool_recycle=3600)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
