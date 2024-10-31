from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from connector.db import Base


class Transactions(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    from_account_id = Column(Integer, ForeignKey('accounts.account_id'))
    to_account_id = Column(Integer, ForeignKey('accounts.account_id' ))
    amount = Column(Integer, nullable=False)
    type = Column(String(255), nullable=False )
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Transaction {self.transaction_id} {self.from_account_id} {self.to_account_id} {self.amount} {self.type} {self.description} >'
    
    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'from_account_id': self.from_account_id,
            'to_account_id': self.to_account_id,
            'amount': self.amount,
            'type': self.type,
            'description': self.description,
            'created_at': self.created_at
        }















# id: (INT, Primary Key) Unique identifier for the transaction.
# from_account_id: (INT, Foreign Key references Accounts.id) Account initiating the transaction (optional for transfers).
# to_account_id: (INT, Foreign Key references Accounts.id) Account receiving the transaction (optional for deposits).
# amount: (DECIMAL(10, 2)) Transaction amount.
# type: (VARCHAR(255)) Type of transaction (e.g., deposit, withdrawal, transfer).
# description: (VARCHAR(255)) Optional description of the transaction.
# created_at: (DATETIME) Timestamp of transaction creation.