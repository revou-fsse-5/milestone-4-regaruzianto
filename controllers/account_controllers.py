from flask import Blueprint, request, jsonify
from models.accounts_model import Accounts
from connector.db import Session
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

accountBP = Blueprint('accountBP', __name__)


@accountBP.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
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
    with Session() as session:
        user = get_jwt_identity()
        user_id = user['id']

        accounts = session.query(Accounts).filter(Accounts.user_id == user_id).all()

        return jsonify([account.to_dict() for account in accounts]), 200

@accountBP.route('/accounts/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
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

            



