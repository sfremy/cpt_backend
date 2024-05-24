from datetime import datetime
from flask import request
from flask_cors import CORS
from __init__ import app, db

from api.user import user_api
from model.users import User
from model.colleges import initColleges

# Create CORS instance before registering blueprint
cors = CORS(app, supports_credentials=True)

# Register blueprint
app.register_blueprint(user_api)

# Flag to ensure initialization only happens once
# initialized = False

@app.before_request
def before_request():
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['localhost:4100', 'http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io']:
        cors._origins = allowed_origin
        
        
# Builds working data for testing
def initUsers():
    with app.app_context():
        """Create database and tables"""
        db.create_all()
        """Tester data for table"""
        u1 = User(name='Lionel Messi', uid='lmessi', email="123@123.com", password='goat', dob=datetime(1847, 2, 11),college_list='[\'Stanford University\', \'MIT\']')
        u2 = User(name='Cristiano Ronaldo', uid='cr7', email="123@123.com", password='123cr7')
        u3 = User(name='Kevin De Bruyne', uid='kdb', email="123@123.com", password='123kdb')
        u4 = User(name='Phil Foden', uid='foden', email="123@123.com", password='123foden')
        u5 = User(name='Rodrigo Hernández', uid='rodri', email="123@123.com", dob=datetime(1920, 10, 21))
        u6 = User(name='Lamine Yamal', uid='yamal', email="123@123.com", dob=datetime(1921, 10, 21))


        users = [u1, u2, u3, u4, u5, u6]

        """Builds sample user/note(s) data"""
        for user in users:
            try:
                '''add user to table'''
                object = user.create()
                print(f"Created new uid {object.uid}")
            except:  # error raised if object nit created
                '''fails with bad or duplicate data'''
                print(f"Records exist uid {user.uid}, or error.")

# SQLAlchemy extracts single user from database matching User ID
def find_by_uid(uid):
    with app.app_context():
        user = User.query.filter_by(_uid=uid).first()
    return user # returns user object

# Check credentials by finding user and verify password
def check_credentials(uid, password):
    # query email and return user record
    user = find_by_uid(uid)
    if user == None:
        return False
    if (user.is_password(password)):
        return True
    return False

# Inputs, Try/Except, and SQLAlchemy work together to build a valid database object
def create():
    # optimize user time to see if uid exists
    uid = input("Enter your user id:")
    user = find_by_uid(uid)
    try:
        print("Found\n", user.read())
        return
    except:
        pass # keep going
    
    # request value that ensure creating valid object
    name = input("Enter your name:")
    password = input("Enter your password")
    email = input("Enter your email:")
    
    # Initialize User object before date
    user = User(name=name, 
                uid=uid, 
                password=password,
                email=email)
    
    # create user.dob, fail with today as dob
    dob = input("Enter your date of birth 'YYYY-MM-DD'")
    try:
        user.dob = datetime.strptime(dob, '%Y-%m-%d').date()
    except ValueError:
        user.dob = datetime.today()
        print(f"Invalid date {dob} require YYYY-mm-dd, date defaulted to {user.dob}")
           
    # write object to database
    with app.app_context():
        try:
            object = user.create()
            print("Created\n", object.read())
        except:  # error raised if object not created
            print("Unknown error uid {uid}")
            
            
# SQLAlchemy extracts all users from database, turns each user into JSON
def read():
    with app.app_context():
        table = User.query.all()
    json_ready = [user.read() for user in table] # "List Comprehensions", for each user add user.read() to list
    return json_ready

# read()
        
# create()                
initUsers()
initColleges()

if __name__ == "__main__":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./volumes/sqlite.db"
    app.run(debug=True, host="0.0.0.0", port="8086")