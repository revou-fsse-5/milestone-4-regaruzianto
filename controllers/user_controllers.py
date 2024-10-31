from flask import Blueprint, request, jsonify
from models.users_model import Users
from connector.db import Session
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
import datetime

userBP = Blueprint('userBP', __name__)

@userBP.route('/users', methods=['POST'])
def create_user():
  """
    Create a new user
    ---
    tags:
      - Users
    summary: Create a new user
    description: This endpoint allows you to create a new user by providing a username, email, and password.
    parameters:
      - in: body
        name: body
        required: True
        schema:
          type: object
          properties:
            username:
              type: string
              example: johndoe
            email:
              type: string
              example: johndoe@example.com
            password:
              type: string
              example: password123
          required:
            - username
            - email
            - password
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: user created successfully
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            message:
              type: string
              example: Missing required fields
      500:
        description: Failed to create user
        schema:
          type: object
          properties:
            error:
              type: string
              example: Failed to create user
    """

  data = request.get_json()

  if data is None:
    return {'message': 'No input data provided'}, 400

  if 'username' not in data or 'email' not in data or 'password' not in data:
    return {'message': 'Missing required fields'}, 400

  with Session() as session:
    try:
      user = Users(username=data['username'], email=data['email'])
      user.set_password(data['password'])

      session.add(user)
      session.commit()

      return jsonify({'message': f'user {data["username"]} created successfully'}),201
    except Exception as e:
      print(e)
      session.rollback()
      return jsonify({'error': "Failed to create user"}),500
        
@userBP.route('/users/login', methods={'POST'})
def login_user():
  """
    Login user
    ---
    tags:
      - Users

    description: Login user

    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: john@example.com
            password:
              type: string
              example: john1234


    responses:
      201:
        description: User logged in successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "User logged in successfully"
            access_token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyZjMxYmQ1ZjE3ZmVhZjEwNjIyZDkwZSIsImlhdCI6MTY3NjMwNjUyMSwiZXhwIjoxNjc2NDA0NTIxfQ.0n5rOJnKUkKv4fV2a-9QX5qGKpL7kR9xjv4RjJNQcE"
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Missing required fields"
      500:
        description: Server error
        schema:
          type: object
          properties:    
            error:
              type: string
              example: "Failed to login user"
    
    """

  data= request.get_json()

  if data is None:
    return jsonify({'error':'No data received'}),400
    
  if 'email' not in data or 'password' not in data:
    return jsonify({'error':'Missing required fields'}),400
    
  with Session() as session:
    try:
      user = session.query(Users).filter(Users.email == data['email']).first()

      if user and user.check_password(data['password']):

        expires = datetime.timedelta(minutes=60)

        access_token = create_access_token(identity={
        'id': user.id,
        'username': user.username,
        'email': user.email 
        }, expires_delta=expires)

        return jsonify({
          'message':f'User logged in successfully',
          'access_token': access_token
        }), 201
    
      return jsonify({'error':'Invalid email or password'}),401
    except Exception as e:
      print(e)
      return jsonify({'error':'Failed to login user'}),500
        
@userBP.route('/users/me', methods=["GET"])
@jwt_required()
def get_user_profile():
  """
    Get the current user's profile
    ---
    tags:
      - Users
    summary: Retrieve the profile of the authenticated user
    description: This endpoint retrieves the profile information of the currently authenticated user using JWT.

    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer token for JWT authentication.

    responses:
      200:
        description: User profile retrieved successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            username:
              type: string
              example: johndoe
            email:
              type: string
              example: johndoe@example.com
            created_at:
              type: string
              format: date-time
              example: '2024-01-01T12:00:00Z'
            updated_at:
              type: string
              format: date-time
              example: '2024-01-01T12:00:00Z'
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: User not found
    """

  with Session() as session:
    try:
      user = get_jwt_identity()
  
      user_id = user['id']
  
      user_profile = session.query(Users).filter(Users.id == user_id).first()
  
      if user_profile:
        return jsonify({
          'id': user_profile.id,
          'username': user_profile.username,
          'email': user_profile.email,
          'created_at': user_profile.created_at,
          'updated_at': user_profile.update_at
        }), 200
      return jsonify({'error': 'User not found'}), 404
    except Exception as e:
      print(e)
      return jsonify({'error': 'Failed to retrieve user profile'}), 500
    
    
@userBP.route('/users/me', methods=['PUT'])
@jwt_required()
def update_user():
  """
    Update the current user's profile
    ---
    tags:
      - Users
    summary: Update the authenticated user's profile information
    description: This endpoint allows the authenticated user to update their profile information, such as username and email.
    parameters:
      - in: header
        name: Authorization
        required: true
        type: string
        description: Bearer token for JWT authentication.

      - in: body
        name: body
        required: True
        schema:
          type: object
          properties:
            username:
              type: string
              example: johndoe123
            email:
              type: string
              example: johndoe123@example.com
    responses:
      200:
        description: User profile updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: User updated successfully
            id:
              type: integer
              example: 1
            username:
              type: string
              example: johndoe123
            email:
              type: string
              example: johndoe123@example.com
            created_at:
              type: string
              format: date-time
              example: '2024-01-01T12:00:00Z'
            updated_at:
              type: string
              format: date-time
              example: '2024-01-01T12:00:00Z'
      404:
        description: User not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: User not found
      400:
        description: Invalid input data
        schema:
          type: object
          properties:
            error:
              type: string
              example: Invalid input data
    """

  data = request.get_json()

  with Session() as session:
    try:
      user = get_jwt_identity()

      user_id = user['id']

      user_profile = session.query(Users).filter(Users.id == user_id).first()

      if not user_profile:
        return jsonify({'error':'User not found'}),404
        
      user_profile.username = data.get('username', user_profile.username)
      user_profile.email = data.get('email', user_profile.email)

      session.commit()

      return jsonify({
        'message':'User updated successfully',
        'username': f'{data["username"]}', #prevent rollback if return user_profile.username
        'email': f'{data["email"]}'
        }),200
    except Exception as e:
      print(e)
      return jsonify({'error': 'Failed to update user profile'}), 500





   
        


                

               
            

    