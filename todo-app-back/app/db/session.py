from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings


settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
sessionlocal = sessionmaker(bind=engine)



def get_db():
    db = sessionlocal()
    try:
        yield db
    except Exception:
        db.rollbacj()
        raise
    finally:
        db.close()