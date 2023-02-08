from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

string_connection = "mysql+mysqldb://"
database_user = f"{config('DATABASE_USER')}:{config('DATABASE_PASSWORD')}@"
database_hostname = f"{config('DATABASE_HOSTNAME')}:{config('DATABASE_PORT')}/"
database_name = f"{config('DATABASE_NAME')}"

SQLALCHEMY_DATABASE_URL = (
    string_connection + database_user + database_hostname + database_name
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, pool_recycle=3600)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
