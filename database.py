from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import settings

db_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# db_url = "postgresql://postgres:postgres@localhost:5432/chronic"
engine = create_engine(db_url)
SessionLocale = sessionmaker(autoflush=False,autocommit=False, bind=engine)

def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()
