""" database dependencies to support sqlite examples """
import datetime
from datetime import datetime
import json

from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=False, nullable=False)
    _uid = db.Column(db.String(255), unique=True, nullable=False)
    _password = db.Column(db.String(255), unique=False, nullable=False)
    _dob = db.Column(db.Date)
    _email = db.Column(db.String(255), unique=False, nullable=False)
    _college_list = db.Column(db.String(255), unique=False, nullable=False)

    def __init__(self, name, uid, email, password="123qwerty", dob=datetime.today(), college_list='[]'):
        self._name = name
        self._uid = uid
        self.set_password(password)
        if isinstance(dob, str):
            dob = date=datetime.today()
        self._dob = dob
        self._email = email
        self._college_list = college_list

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @property
    def uid(self):
        return self._uid
    
    @uid.setter
    def uid(self, uid):
        self._uid = uid
    
    @property
    def password(self):
        return self._password[0:10] + "..."
    
    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, method="pbkdf2:sha256")

    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    @property
    def dob(self):
        dob_string = self._dob.strftime('%m-%d-%Y')
        return dob_string
    
    @dob.setter
    def dob(self, dob):
        if isinstance(dob, str):  
            dob = date=datetime.today()
        self._dob = dob
                
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        self._email = email
        
    @property
    def college_list(self):
        return self._college_list
    
    @college_list.setter
    def college_list(self, college_list):
        self._college_list = college_list
    
    @property
    def age(self):
        today = datetime.today()
        return today.year - self._dob.year - ((today.month, today.day) < (self._dob.month, self._dob.day))
    
    def __str__(self):
        return json.dumps(self.read())

    def create(self):
        try:
            db.session.add(self)  
            db.session.commit()  
            return self
        except IntegrityError:
            db.session.remove()
            return None

    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "uid": self.uid,
            "dob": self.dob,
            "age": self.age,
            "email": self.email,
            "college_list": self.college_list
        }

    def update(self, name="", uid="", password="",email="",college_list=""):
        """only updates values with length"""
        if len(name) > 0:
            self.name = name
        if len(uid) > 0:
            self.uid = uid
        if len(password) > 0:
            self.set_password(password)
        if len(email) > 0:
            self.email = email
        if len(college_list) > 0:
            self.college_list = college_list
        db.session.add(self) 
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None