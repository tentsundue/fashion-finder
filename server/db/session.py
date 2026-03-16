from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from server.config import settings


engine = create_engine(settings.DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db = SessionLocal()

    try:
        yield db
    except Exception as e:
        print(e)
    finally:
        db.close()
