from connector.db import Base, Session
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship


class Accounts(Base):
    
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    account_type = Column(String(255), nullable=False )
    account_number = Column(Integer,  nullable=False, unique=True)
    balance = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    update_at= Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    transactions_from = relationship('Transactions', backref='accounts_from', lazy=True, foreign_keys='Transactions.from_account_id')
    transactions_to = relationship('Transactions', backref='accounts_to', lazy=True, foreign_keys='Transactions.to_account_id')

    def __repr__(self):
        return f'<Account {self.account_id} {self.account_type} {self.account_number} {self.balance} >'

    
    def set_account_number(self):
        with Session() as session:
            last_account = session.query(Accounts).order_by(Accounts.account_id.desc()).first() 

            if last_account is None:
                self.account_number = 1
            else:
                self.account_number = last_account.account_number + 1
        
            return self.account_number

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'account_type': self.account_type,
            'account_number': self.account_number,
            'balance': self.balance,
            'created_at': self.created_at,
            'updated_at': self.update_at
        }

# id: (INT, Primary Key) Unique identifier for the account.
# user_id: (INT, Foreign Key references Users.id) User associated with the account.
# account_type: (VARCHAR(255)) Type of account (e.g., checking, savings).
# account_number: (VARCHAR(255), Unique) Unique account number.
# balance: (DECIMAL(10, 2)) Current balance of the account.
# created_at: (DATETIME) Timestamp of account creation.
# updated_at: (DATETIME) Timestamp of account information update.