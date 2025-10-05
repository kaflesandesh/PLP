from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Text, DateTime
from datetime import datetime

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
    
    # Add this inside the User class to define the chat history relationship
    chat_history = relationship("ChatHistory", order_by="ChatHistory.timestamp", back_populates="user")

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    instructor_id = Column(Integer, ForeignKey('users.id'))
    instructor = relationship('User')
    enrollments = relationship('Enrollment', back_populates='course')

class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    status = Column(String, default='pending')
    student = relationship('User')
    course = relationship('Course', back_populates='enrollments')

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

class ChatHistory(Base):
    __tablename__ = 'chat_history'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(Text, nullable=False)
    is_user = Column(Integer, default=1)  # 1 if user message, 0 if AI tutor response
    timestamp = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="chat_history")

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