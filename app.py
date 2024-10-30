from flask import Flask
from models.users_model import Users
from models.accounts_model import Accounts
from models.transactions_model import Transactions
from controllers.account_controllers import accountBP
from controllers.user_controllers import userBP
from controllers.transaction_controllers import transactionBP
from connector.db import Base,engine
from flask_jwt_extended import JWTManager
import os
from flasgger import Swagger


Base.metadata.create_all(engine)

app= Flask(__name__)

jwt = JWTManager(app)
swagger = Swagger(app)

app.register_blueprint(userBP)
app.register_blueprint(accountBP)
app.register_blueprint(transactionBP)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def hello_world():
    return 'Hello World!'