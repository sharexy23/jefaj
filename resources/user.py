from db import db
import hashlib
from models.user import *
#from models.transfers import Transfer
from flask import jsonify
from flask_restful import Resource, reqparse
#from flask_jwt import jwt_required
from flask_jwt_extended import create_access_token,create_refresh_token,jwt_required
#from flask_mail import *


class register(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('middlename',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('date_of_birth',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pin',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def encrypt_string(hash_string):
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature

    def post(self):
        data = register.parser.parse_args()
        if Ujer.find_by_phone_number(data['phone_number']):
            return  {'message':'user exists'},400

        user = Ujer(data['phone_number'],data['firstname'],data['middlename'],data['lastname'],data['date_of_birth'],
        data['password'],data['email'],data['pin'],'00')

        user.password = register.encrypt_string(user.password)
        #dk = hashlib.pbkdf2_hmac('sha256', b'password', b'salt', 100000)
        #user.password = user.password
        #dk.hex(user.password)
        user.pin = register.encrypt_string(user.pin)
        #user.transfer = list(user.transfer)
        #user.pin = encrypt_string(user.pin)

        Ujer.save_to_db(user)
        return {
        'status': True,
        'data': user.json(),
        'message':'message'
        },201

class login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    def post(self):
        data = login.parser.parse_args()
        user = Ujer.find_by_phone_number(data['phone_number']) and Ujer.find_by_password(data['password'])
        if user:
            access_token = create_access_token(identity=user.id,fresh =True)
            refresh_token= create_refresh_token(user.id)
            return {
                  'status': True,
                  'access_token': access_token,
                  'message':'you are logged in'
            },200
        return {
        'status':True,
        'status':False,
        'message':'user not found'
        },400


class account_balance(Resource):
#    global users
    #@jwt_required()
    def get(self, phone_number):
        user = Ujer.find_by_phone_number(phone_number)
        if user:
            return jsonify(user.money_in_the_bag)
    #    return {'user': 'does not exist'}
        return {
        'status':True,
        'user': 'does not exist'
        },404


class Top_up(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('ammount',
                        type= float,
                        required=True,
                        help="This field cannot be left blank!"
                        )


    @jwt_required
    def put(self):
        data = Top_up.parser.parse_args()
        user = Ujer.find_by_phone_number(data['phone_number'])
        #user.money_in_the_bag = float(user.money_in_the_bag)
        if user:
            user.money_in_the_bag = float(user.money_in_the_bag)
            user.money_in_the_bag = data['ammount'] + user.money_in_the_bag
            user.money_in_the_bag =str(user.money_in_the_bag)
            Ujer.save_to_db(user)
            return jsonify(user.money_in_the_bag)
        return{'message':'wo geddifok'}


class transfer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('source_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('destination_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pin',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('ammount',
                        type= float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('description',
                        type= str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('destination_phone_number',
                        type= str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('user_id',
                        type= int,
                        required=True,
                        help="every transfer needs a user"
                        )

    #@jwt_required
    def post(self):
        data = transfer.parser.parse_args()

        user = Ujer.find_by_phone_number(data['phone_number'])
        #user = User.find_by_pin(data['pin'])
        destination = Ujer.find_by_phone_number(data['destination_phone_number'])

        #user.money_in_the_bag = float(user.money_in_the_bag)
        #destination.money_in_the_bag = float(destination.money_in_the_bag)



        if user is not None and destination is not None:
            user.money_in_the_bag = float(user.money_in_the_bag)
            destination.money_in_the_bag = float(destination.money_in_the_bag)
            if user.money_in_the_bag < data['ammount']:
                return {'message':'get a job'}


            destination.money_in_the_bag = data['ammount'] + destination.money_in_the_bag
            user.money_in_the_bag = data['ammount'] - user.money_in_the_bag
            user.money_in_the_bag = str(user.money_in_the_bag)
            destination.money_in_the_bag = str(destination.money_in_the_bag)
            transferg = Transfer(data['source_name'],data['destination_name'],"a money transfer",data['destination_phone_number'],data['phone_number'],data['ammount'],data['user_id'])
            Transfer.save_to_db(transferg)
            Ujer.save_to_db(user)
            #user.transfers = user.transfers + ('j')
            return {'message':'money don comot for your account'}
        return {'message':'dh'}



class TransferHistory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('phone_number',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    #it seems to me that this function is cur

    def post(self):
        data = TransferHistory.parser.parse_args()
        user = Ujer.find_by_phone_number(data['phone_number'])
        if user:
            return user.json()
        return {'message':'money done commot for your account'}
