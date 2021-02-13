import os
from flask import Flask,jsonify,request,render_template
from flask_restful import Api,Resource, reqparse
from resources.user import *
from db import db
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '!@#$%^&*()_+=-0987654321'
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_table():
    db.create_all()


api.add_resource(register, '/register')
api.add_resource(login, '/login')
api.add_resource(account_balance, '/balance/<string:phone_number>')
api.add_resource(Top_up, '/add_money')
api.add_resource(transfer, '/transfer')
api.add_resource(TransferHistory, '/transfers')
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port =5000 , debug =True)
