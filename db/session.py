from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://dungbb:123456@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine)
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
