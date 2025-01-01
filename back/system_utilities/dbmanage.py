from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()
metadata = MetaData()
engine = create_engine('sqlite:///plp.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    type = Column(String)

class UserInformation(Base):
    __tablename__ = 'user_information'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    dob = Column(Date)
    address = Column(String)
    phone = Column(String)
    email = Column(String, unique=True)
    major = Column(String)
    user = relationship("User")

class Log(Base):
    __tablename__ = 'activity_log'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    action = Column(String)
    message = Column(String)
    user = relationship("User")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables_if_not_exist():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables created")
    except SQLAlchemyError as e:
        print(f"Error creating tables: {e}")
