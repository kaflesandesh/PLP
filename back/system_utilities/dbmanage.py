from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///plp.db"  # SQLite database file

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example usage
if __name__ == "__main__":
    # Create a new session
    db = next(get_db())
    
    # Perform database operations using `db`
    # For example, to query the database:
    # result = db.query(SomeModel).all()
    
    # Don't forget to close the session
    db.close()
