from flask import Blueprint, request, jsonify
from models.transactions_model import Transactions
from models.accounts_model import Accounts
from connector.db import Session
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from sqlalchemy import or_
import datetime


transactionBP = Blueprint('transactionBP', __name__)

@transactionBP.route('/users/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
  """
    Get all transactions
    ---
    tags:
      - Transactions
    summary: Get all transactions
    description: This endpoint allows you to get all transactions.

    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer token for JWT authentication.

    responses:
      200:
        description: Get all transactions
        schema:
          type: object
          properties:
            transactions:
              type: array
              items:
                type: object
                properties:
                  transaction_id:
                    type: integer
                    example: 1
                  from_account_id:
                    type: integer
                    example: 1
                  to_account_id:
                    type: integer
                    example: 2
                  amount:
                    type: integer
                    example: 100
                  type:
                    type: string
                    example: deposit
                  description:
                    type: string
                    example: deposit
                  created_at:   
                    type: string
                    example: 2022-01-01

    """
  user = get_jwt_identity()
  user_id = user['id']

  with Session() as session:
    accounts = session.query(Accounts).filter(Accounts.user_id == user_id).all()

    if accounts is None:
      return jsonify({'error':'No Account found'}),400
        
    account_ids = [account.account_id for account in accounts]

    transactions = session.query(Transactions).filter(or_(Transactions.to_account_id.in_(account_ids),Transactions.from_account_id.in_(account_ids))).all()
    print(transactions)
        
    return jsonify([transaction.to_dict() for transaction in transactions]), 200



@transactionBP.route('/users/transactions/accounts/<int:account_id>', methods=['GET'])
@jwt_required()
def get_transactions_by_account(account_id):

  """
  Get transactions by account ID
  ---
  tags:
    - Transactions
  summary: Get all transactions by account ID
  description: This endpoint allows you to get all transactions by account ID.
  
  parameters:
    - in: header
      name: Authorization
      required: true
      type: string
      description: Bearer token for JWT authentication.

    - in: path
      name: account_id
      required: true
      type: integer
      
  responses:
    200:
      description: Get all transactions
      schema:
        type: object
        properties:
          transactions:
            type: array
            items:
              type: object
              properties:
                transaction_id:
                  type: integer
                  example: 1
                from_account_id:
                  type: integer
                  example: 1
                to_account_id:
                  type: integer 
                  example: 2
                amount:
                  type: integer
                  example: 100
                type:
                  type: string
                  example: deposit
                description:
                  type: string
                  example: deposit
                created_at:   
                  type: string
                  example: 2022-01-01
  """

  user = get_jwt_identity()
  user_id = user['id']

  with Session() as session:
    try:
      # Memeriksa apakah akun milik pengguna
      account = session.query(Accounts).filter(Accounts.user_id == user_id, Accounts.account_id == account_id).first()

      if account is None:
        return jsonify({'error': 'Account not found'}), 404

      # Memeriksa transaksi yang terkait dengan akun tersebut
      transactions = session.query(Transactions).filter(or_(Transactions.to_account_id == account_id,Transactions.from_account_id == account_id)).all()
            

      return jsonify([transaction.to_dict() for transaction in transactions]), 200
    except Exception as e:
      print(e)
      return jsonify({'error': 'Failed to retrieve transactions'}), 500
        


@transactionBP.route('/users/transactions/accounts/<int:account_id>/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction_by_transactionID(account_id, transaction_id):
  """
  Get transaction by transaction ID
  ---
  tags:
    - Transactions
  summary: Get transaction by transaction ID
  description: This endpoint allows you to get transaction by transaction ID.
  
  parameters:
    - in: header
      name: Authorization
      required: true
      type: string
      description: Bearer token for JWT authentication.

    - in: path
      name: account_id
      required: true
      type: integer
      
    - in: path  
      name: transaction_id
      required: true
      type: integer
      
  responses:
    200:
      description: Get all transactions
      schema:
        type: object  
        properties:
          transaction:
            type: object
            properties:
              transaction_id:
                type: integer
                example: 1
              from_account_id:
                type: integer
                example: 1
              to_account_id:
                type: integer 
                example: 2
              amount:
                type: integer
                example: 100
              type:
                type: string
                example: deposit
              description:
                type: string
                example: deposit
              created_at:   
                type: string
                example: 2022-01-01
  """

  user = get_jwt_identity()
  user_id = user['id']

  with Session() as session:
    try:
      # Memeriksa apakah akun milik pengguna
      account = session.query(Accounts).filter(Accounts.user_id == user_id, Accounts.account_id == account_id).first()

      if account is None:
        return jsonify({'error': 'Account not found'}), 404
            
      # Memeriksa transaksi yang terkait dengan akun tersebut
      transaction = session.query(Transactions).filter(Transactions.transaction_id == transaction_id, or_(Transactions.to_account_id == account_id,Transactions.from_account_id == account_id)).first()

      if transaction is None:
        return jsonify({'error': 'Transaction not found'}), 404

      return jsonify(transaction.to_dict()), 200
    except Exception as e:
      print(e)
      return jsonify({'error': 'Failed to retrieve transaction'}), 500
    


@transactionBP.route('/users/transactions/deposit', methods=['POST'])
@jwt_required()
def deposit():
  """
  Deposit to account
  ---
  tags:
    - Transactions
  summary: Deposit to account
  description: This endpoint allows you to deposit to account.
  parameters:
    - in: header
      name: Authorization
      required: true
      type: string
      description: Bearer token for JWT authentication.

    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          to_account_id:
            type: integer
            example: 1
          amount:
            type: integer
            example: 100
          description:
            type: string
            example: deposit
          type:
            type: string
            example: deposit
  responses:
    200:
      description: Deposit successful
      schema:
        type: object
        properties: 
          message:
            type: string
            example: Deposit successful

    404:
      description: Account not found
      schema:
        type: object
        properties:
          error:
            type: string
            example: Account not found
  """
  user = get_jwt_identity()
  user_id = user['id']

  with Session() as session:
    try:
      data = request.get_json()
      to_account_id = data.get('to_account_id')
      amount = data.get('amount')
      description = data.get('description')
      type = 'deposit'
      amount_int = int(amount)
      
      # Memeriksa apakah akun milik pengguna
      account = session.query(Accounts).filter(Accounts.user_id == user_id, Accounts.account_id == to_account_id).first()

      if account is None:
        return jsonify({'error': 'Account not found'}), 404

      # buat transaksi deposit
      transaction = Transactions(to_account_id=to_account_id, amount=amount, description=description, type=type)
      account.balance += amount_int

      session.add(transaction)
      session.commit()

      return jsonify({'message': 'Deposit successful'}), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to deposit'}), 500



@transactionBP.route('/users/transactions/withdrawal', methods=['POST'])
@jwt_required()
def withdrawal():
  """
  Withdrawal from account
  ---
  tags:
    - Transactions
  summary: Withdrawal from account
  description: This endpoint allows you to withdrawal from account.
  parameters:
    - in: header
      name: Authorization
      required: true
      type: string
      description: Bearer token for JWT authentication.

    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          from_account_id:
            type: integer
            example: 1
          amount: 
            type: integer
            example: 100
          description:
            type: string
            example: withdrawal
          type:
            type: string
            example: withdrawal
  responses:
    200:
      description: Withdrawal successful
      schema:
        type: object
        properties: 
          message:
            type: string
            example: withdrawal successful

    404:
      description: Account not found
      schema:
        type: object
        properties:
          error:
            type: string
            example: Account not found

  """

  data = request.get_json()
  user = get_jwt_identity()
  user_id = user['id']

  with Session() as session:
    try:
      from_account_id = data.get('from_account_id')
      amount = data.get('amount')
      description = data.get('description')
      type = 'withdrawal'
      amount_int = int(amount)

            
      # Memeriksa akun milik pengguna
      account = session.query(Accounts).filter(Accounts.user_id == user_id, Accounts.account_id == from_account_id).first()

      if account is None:
        return jsonify({'error':'Account not found'}),400
            

      if account.balance < amount_int:
        return jsonify({'message':'Insufficient Balance'}),400
            
      transaction= Transactions(from_account_id = from_account_id, amount = amount, description = description, type = type)
      account.balance -= amount_int
            
      session.add(transaction)
      session.commit()

      return jsonify({'message':'withdrawal succesfull'}),200
    except Exception as e:
      print(e)
      return jsonify({'error':'Something wrong happen failed to withdrawal'}),500
        


@transactionBP.route('/users/transactions/transfer', methods=['POST'])
@jwt_required()
def transfer():
  """
  Transfer from one account to another
  ---
  tags:
    - Transactions
  summary: Transfer from one account to another
  description: This endpoint allows you to transfer from one account to another.
  parameters:
    - in: header
      name: Authorization
      required: true
      type: string
      description: Bearer token for JWT authentication.

    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          from_account_id:
            type: integer
            example: 1
          to_account_id: 
            type: integer
            example: 2
          amount: 
            type: integer
            example: 100
          description:
            type: string
            example: transfer
          type:
            type: string
            example: transfer
  responses:
    200:
      description: Transfer successful
      schema:
        type: object
        properties: 
          message:
            type: string
            example: transfer successful

    404:
      description: Account not found
      schema:
        type: object
        properties:
          error:
            type: string
            example: Account not found

  """

  data = request.get_json()

  user = get_jwt_identity()
  user_id = user['id']

  with Session() as session:
    try:

      from_account_id = data.get('from_account_id')
      to_account_id = data.get('to_account_id')
      amount = data.get('amount')
      description = data.get('description')
      type = 'transfer'
      amount_int = int(amount)

      # Memeriksa akun milik pengguna
      account = session.query(Accounts).filter(Accounts.user_id == user_id, Accounts.account_id == from_account_id ).first()

      # Memeriksa akun yang akan di transfer
      account_to_transfer = session.query(Accounts).filter(Accounts.account_id == to_account_id).first()

      if account is None:
        return jsonify({'error':'Account not found'}),400

      if account_to_transfer is None:
        return jsonify({'error':'Invalid Account ID to transfer'}),400

      if account.balance < amount_int:
        return jsonify({'error':'Insufficient Balance'}),400

      transaction = Transactions(from_account_id=from_account_id, to_account_id=to_account_id, amount=amount, type=type, description=description)

      account.balance -= amount_int
      account_to_transfer.balance += amount_int

      session.add(transaction)
      session.commit()
      return jsonify({'message':'transfer successfull'}),200
    except Exception as e:
      print(e)
      return jsonify({'error':'Something wrong happen Failed to transfer'}),500
        






# GET /transactions: Retrieve a list of all transactions for the currently authenticated user's accounts. (Optional: filter by account ID, date range)
# GET /transactions/:id: Retrieve details of a specific transaction by its ID. (Authorization required for related account owner)
# POST /transactions: Initiate a new transaction (deposit, withdrawal, or transfer). (Authorization required for related account owner)

# id: (INT, Primary Key) Unique identifier for the transaction.
# from_account_id: (INT, Foreign Key references Accounts.id) Account initiating the transaction (optional for transfers).
# to_account_id: (INT, Foreign Key references Accounts.id) Account receiving the transaction (optional for deposits).
# amount: (DECIMAL(10, 2)) Transaction amount.
# type: (VARCHAR(255)) Type of transaction (e.g., deposit, withdrawal, transfer).
# description: (VARCHAR(255)) Optional description of the transaction.
# created_at: (DATETIME) Timestamp of transaction creation.