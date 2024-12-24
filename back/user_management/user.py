from sqlalchemy import Column, Integer, String
from back.system_utilities.dbmanage import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    type = Column(String)  # 'student', 'instructor', 'admin'

    def __init__(self, name, email, password, user_type):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.type = user_type

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
