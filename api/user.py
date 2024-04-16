import jwt
from model.users import User
from model.colleges import College
from flask import Blueprint, request, jsonify, current_app, Response, session
from flask_restful import Api, Resource
from datetime import datetime
from auth_middleware import token_required
import json

user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)

class UserAPI:
    class _CRUD(Resource):
        def post(self):  # Removed current_user
            body = request.get_json()

            # Validate inputs
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 400

            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 400

            password = body.get('password')
            dob = body.get('dob')
            email = body.get('email')

            uo = User(name=name, uid=uid, email=email)

            if password is not None:
                uo.set_password(password)

            if dob is not None:
                try:
                    uo.dob = datetime.strptime(dob, '%Y-%m-%d').date()
                except:
                    return {'message': f'Date of birth format error {dob}, must be mm-dd-yyyy'}, 400

            # Add user to database
            user = uo.create()

            if user:
                return jsonify(user.read())  # 201 Created status code

            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 400

        @token_required
        def get(self, current_user):  # Read method
            users = User.query.all()  # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

        @token_required
        def delete(self, current_user):
            body = request.get_json()
            uid = body.get('uid')
            users = User.query.all()

            for user in users:
                if user.uid == uid:
                    user.delete()
            return jsonify(user.read())

    class _Edit(Resource):
        # POST method to add new colleges to a user's list
        def post(self):
            # Retrieve the user's ID from the session to identify the user making the request
            username = session.get('uid')
            # Query the database for the user's record using the user ID
            user = User.query.filter_by(_uid=username).first()
            
            if user is None:
                return {'message': "Invalid user id"}, 400
            
            # Decode the JSON string of the user's college list into a Python list
            namelist = json.loads(user.college_list)
            # Query the database for colleges that match the names in the user's list
            matching_colleges = College.query.filter(College.name.in_(namelist)).all()
            # Convert the query results to a JSON-serializable format
            colleges_data = [college.read() for college in matching_colleges]
            json_data = jsonify(colleges_data)
            
            return json_data  # Return the JSON data of the colleges

        # GET method to retrieve a list of all colleges from the database
        def get(self):
            # Query the database for all college records
            all_colleges = College.query.all()
            # Convert each college record to a JSON-serializable format
            colleges_data = [college.read() for college in all_colleges]
            json_data = jsonify(colleges_data)
            
            return json_data  # Return the JSON data of all colleges

        # PUT method to update the college list associated with a user
        def put(self):
            # Retrieve the user's ID from the session
            username = session.get('uid')
            # Query the database for the user's record
            user = User.query.filter_by(_uid=username).first()
            
            if user is None:
                return {'message': "Invalid user id"}, 400
            
            # Decode the JSON string of the user's current college list into a Python list
            namelist = json.loads(user.college_list)
            # Extract data from the request's JSON body
            body = request.get_json()
            # Get the list of college names from the request data
            selected_names = body.get('names', [])
            
            # Update the user's college list by adding new names, avoiding duplicates
            namelist += [elem for elem in selected_names if elem not in namelist]
            # Update the user's record in the database with the new college list
            user.update_list(json.dumps(namelist))

    class _Security(Resource):
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                session['uid'] = uid
                
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')

                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        token_payload = {
                            "_uid": user._uid,
                        }
                        token = jwt.encode(
                            token_payload,
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        resp = Response("Authentication for %s successful" % (user._uid))
                        resp.set_cookie("jwt", token,
                                        max_age=3600,
                                        secure=True,
                                        httponly=True,
                                        path='/',
                                        samesite='None'  # This is the key part for cross-site requests

                                        # domain="frontend.com"
                                        )
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                    "message": "Something went wrong!",
                    "error": str(e),
                    "data": None
                }, 500

    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Edit, '/edit')