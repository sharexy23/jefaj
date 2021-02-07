from db import db

class User(db.Model):
    __TableName__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(11))
    firstname = db.Column(db.String(80))
    middlename = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    date_of_birth = db.Column(db.String(60))
    password = db.Column(db.String(80))
    email = db.Column(db.String(80))
    pin = db.Column(db.String(4))
    money_in_the_bag = db.Column(db.String)
    transfer = db.column(db.String)
    #verification_code = db.Column(db.String(80))

    def __init__(self, phone_number, firstname,middlename,lastname,date_of_birth, password,email,pin, money_in_the_bag,transfer):
        #self.id = _id
        self.phone_number = phone_number
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.password = password
        self.email = email
        self.pin = pin
        self.money_in_the_bag = money_in_the_bag
        self.transfer = transfer
        #self.verification_code = verification_code

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {'phone_number':self.phone_number,'firstname':self.firstname,'middlename':self.middlename,'lastname':self.lastname,'date_of_birth':self.date_of_birth,'password':self.password,'email':self.email,'pin':self.pin}

    @classmethod
    def find_by_password(cls, password):
        return cls.query.filter_by(password=password).first()

    @classmethod
    def find_by_phone_number(cls, phone_number):
        return cls.query.filter_by(phone_number = phone_number).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_pin(cls, pin):
        return cls.query.filter_by(pin=pin).first()
