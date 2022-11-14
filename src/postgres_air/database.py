from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from postgres_air.config import settings

user = settings.POSTGRES_USER
password = settings.POSTGRES_PASSWORD
host = settings.POSTGRES_HOST
port = settings.DATABASE_PORT
db = settings.POSTGRES_DB

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{db}"


def get_session():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'options': '-csearch_path={}'.format(db)})
    session = Session(bind=engine.connect())
    try:
        yield session
    finally:
        session.close()
