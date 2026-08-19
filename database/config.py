
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DORIXONA_URL = "sqlite:///./dorixona.db"

engine = create_engine(DORIXONA_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


