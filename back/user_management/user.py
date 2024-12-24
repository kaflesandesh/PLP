from sqlalchemy import Column, Integer, String
from back.dbmanage import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    type = Column(String)  # e.g., 'student', 'instructor', 'admin'

    def __init__(self, name, email, user_type):
        self.name = name
        self.email = email
        self.type = user_type
