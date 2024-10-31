from flask import Blueprint, request, jsonify
from models.accounts_model import Accounts
from connector.db import Session
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

accountBP = Blueprint('accountBP', __name__)


@accountBP.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
  """
    create a new account
    ---
    tags:
      - Accounts
    summary: Create a new account
    description: This endpoint allows you to create a new account by providing an account type.
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
            account_type:
              type: string
              example: savings
    responses:
      201:
        description: Account created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: account created successfully
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            error:
              type: string
              example: Missing required fields
  """
  data = request.get_json()
  user = get_jwt_identity()
  userid = user['id']

  if data is None:
    return {'message': 'No input data provided'}, 400

  if 'account_type' not in data:
    return {'message': 'Missing required fields'}, 400

  with Session() as session:
    try:
      account = Accounts(
        user_id=userid,
        account_type=data['account_type'],
        balance=0,
      )
      account.set_account_number()
      session.add(account)
      session.commit()

      return jsonify({'message': f'{account.account_type} account created successfully'}), 201
    except Exception as e:
      print(e)
      session.rollback()
      return jsonify({'error': "Failed to create account"}), 500



@accountBP.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
  """
    get account
    ---
    tags:
      - Accounts
    summary: Get account
    description: This endpoint allows you to get accounts.
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer token for JWT authentication.

    responses:
      200:
        description: Get account successfully
        schema:
          type: object
          properties:
            accounts:
              type: array
              items:
                type: object
                properties:
                  account_id:
                    type: integer
                    example: 1
                  account_type:
                    type: string
                    example: savings
                  balance:
                    type: integer
                    example: 100000
                  account_number:
                    type: string
                    example: 10
    """
  with Session() as session:
    user = get_jwt_identity()
    user_id = user['id']

    accounts = session.query(Accounts).filter(Accounts.user_id == user_id).all()

    return jsonify([account.to_dict() for account in accounts]), 200



@accountBP.route('/accounts/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
  """
        get account by account id
        ---
        tags:
          - Accounts
        summary: Get account by Account id
        description: This endpoint allows you to get accounts by account id.
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
            description: Get account successfully
            schema:
              type: object
              properties:
                accounts:
                  type: array
                  items:
                    type: object
                    properties:
                      account_id:
                        type: integer
                        example: 1
                      account_type:
                        type: string
                        example: savings
                      balance:
                        type: integer
                        example: 100000
                      account_number:
                        type: string
                        example: 10
    """
  with Session() as session: 
    user = get_jwt_identity()
    user_id = user['id']

    account = session.query(Accounts).filter(Accounts.user_id == user_id, Accounts.account_id == account_id).first()

    if account is None:
      return jsonify({'error': 'Account not found'}), 404

    return jsonify(account.to_dict()), 200



@accountBP.route('/accounts/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
  """
        Update account
        ---
        tags:
          - Accounts
        summary: Update account
        description: This endpoint allows you to update accounts.
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

          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                account_type:
                  type: string
                  example: checking
        responses:
          201:
            description: Account cupdated successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: account updated successfully
          400:
            description: No data Received
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: No data Received
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
  userid = user['id']
  data = request.get_json()


  if data is None:
    return jsonify({'error':'No data Received'}),400
    
  with Session() as session:
    try:
      account = session.query(Accounts).filter(Accounts.user_id == userid, Accounts.account_id == account_id).first()
      if account is None: 
        return jsonify({'error': 'Account not found'}), 404

      account.account_type = data.get('account_type', account.account_type)
            
      session.commit()
      return jsonify({'message': 'Account updated successfully'}), 200        
    except Exception as e:
      print(e)
      session.rollback()
      return jsonify({'error': 'Failed to update account'}), 500 



@accountBP.route('/accounts/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
  """
        Delete account
        ---
        tags:
          - Accounts
        summary: Delete account
        description: This endpoint allows you to delete account.
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
          201:
            description: Account deleted successfully
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: account updated successfully
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
  userid = user['id']

  with Session() as session:
    try:
      account = session.query(Accounts).filter(Accounts.user_id == userid, Accounts.account_id == account_id).first()
      if account is None: 
        return jsonify({'error': 'Account not found'}), 404

      session.delete(account)
      session.commit()

      return jsonify({'message': 'Account deleted successfully'}), 200
    except Exception as e:  
      print(e)
      session.rollback()
      return jsonify({'error': 'Failed to delete account'}), 500






