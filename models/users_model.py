from connector.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from bcrypt import hashpw, gensalt, checkpw


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(255), nullable=False, unique=True )
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at= Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    accounts = relationship('Accounts', backref='users', lazy=True)

    def __repr__(self):
        return f'<User {self.username} {self.email} {self.password}>'
    
    def set_password(self,password):
        self.password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def check_password(self,password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


