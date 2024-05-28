import json
import ast
import jwt

import pandas as pd
import numpy as np

from datetime import datetime
from flask import Flask, Blueprint, request, jsonify, current_app, Response, session
from flask_cors import CORS
from flask_restful import Api, Resource
from datamodel import datamodel

from model.users import User
from model.colleges import College
from auth_middleware import token_required
from __init__ import db

user_api = Blueprint('user_api', __name__, url_prefix='/api/users')
api = Api(user_api)

app = Flask(__name__)
CORS(app, origins="*")

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
            # Extract data from the request's JSON body
            body = request.get_json()
            
            # Retrieve the user's ID
            username = body.get('name')
            
            if username is None:
                return {'message': 'Invalid request'}, 400
            
            # Query the database for the user's record using the user ID
            user = User.query.filter_by(_uid=username).first()
            
            if user is None:
                return {'message': "User ID not found"}, 404
            
            # Decode the JSON string of the user's college list into a Python list
            namelist = ast.literal_eval(user.read()['college_list'])
            
            # Query the database for colleges that match the names in the user's list
            matching_colleges = College.query.filter(College._name.in_(namelist)).all()
            
            # Convert the query results to a JSON-serializable format
            colleges_data = [college.read() for college in matching_colleges]
            print(colleges_data)
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
        # Extract data from the request's JSON body
            body = request.get_json()
            
            # Print request data for debugging
            print("Request Data:", body)
            
            # Retrieve the user's ID
            user_id = body.get('id')
            
            # DEBUG
            print("User ID:", user_id)
            
            # Query the database for the user's record
            user = User.query.filter_by(_uid=user_id).first()
            
            # DEBUG
            print("User:", user)
            
            if user is None:
                return {'message': "User ID not found"}, 404
            
            # Get the list of college names from the request data
            selected_colleges = body.get('college_list', [])
            
            # Decode the JSON string of the user's current college list into a Python list
            namelist = ast.literal_eval(user.college_list)
            
            print("Existing College List:", namelist) # DEBUG
            
            # Update the user's college list by adding new names, avoiding duplicates
            namelist += [college for college in selected_colleges if college not in namelist]
            
            # Update the user's record in the database with the new college list
            user.update(college_list=json.dumps(namelist))
            
            return {
            'message': "User list updated",
            'id': user.id,
            'college_list': namelist
            }, 200
            
        # NEW STUFF - DELETE COLLEGES FROM LIST

        @token_required # In order to access current_user that required authentication
        def delete(current_user): # To delete colleges from the list
            # Extract data from the request's JSON body
            body = request.get_json()
                    
            # Retrieve the user's ID
            username = body.get('name')
                        
            if username is None:
                return {'message': 'Invalid request'}, 400
                        
            # Query the database for the user's record using the user ID
            user = User.query.filter_by(_uid=username).first()
                        
            if user is None:
                return {'message': "User ID not found"}, 404
            
            # selected_colleges = body.get('college_list', [])
            selected_colleges = json.loads(user.college_list)
            colleges_to_delete = body.get('names')
                    
            if not colleges_to_delete:
                return {'message': 'No colleges to delete provided'}, 400

            # Iterate through the colleges to delete and remove them from the user's selection list
            for college_to_delete in colleges_to_delete:
                if college_to_delete in selected_colleges:
                    selected_colleges.remove(college_to_delete)

            # Update the user's record in the database with the updated selection list
            user.update(college_list=json.dumps(selected_colleges))

            # Commit changes to the database
            # db.session.commit()

            return {'message': 'Colleges deleted successfully'}, 200

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
                }, 400
                
    class _Prediction(Resource):
        def post(self):
            try:
                body = request.get_json()
                # Convert input data to numeric format
                gpa = float(body.get('gpa'))
                SAT = int(body.get('SAT'))
                Extracurricular_Activities = int(body.get('Extracurricular_Activities'))
                Model = datamodel()
                Model.training()
                prediction_result = Model.predict(gpa, SAT, Extracurricular_Activities)
                return jsonify(prediction_result)
            except Exception as e:
                print("Prediction error:", str(e))  # Log the error
                return {
                    "message": "Something went wrong during prediction!",
                    "error": str(e),
                    "data": None
                }, 500
                
        # Order database entries based on weighted match
        def get(self):
            body = request.get_json()
            z_matrix = np.array([])
            value_sum = 0
            try:
                for attribute, value in body.items():
                    # Get the column attribute dynamically
                    column_attr = getattr(College, attribute)
                    # Fetch the column values
                    column_values = np.array([getattr(college, attribute) for college in db.session.query(column_attr).all()])
                    # value[0] is the user-provided value, value[1] is the weighting
                    z_row = (abs((column_values - value[0]))/value[0])*value[1]
                    z_matrix = np.vstack([z_matrix, z_row]) if z_matrix.size else z_row
                    value_sum += value[1]
                
                #Sum weighted deviations for all colleges
                column = getattr(College, '_name')
                names = np.array([getattr(college, '_name') for college in db.session.query(column).all()])
                z_list = z_matrix.sum(axis=0)/value_sum
                
                #Sort names & report matches
                unsorted = dict(zip(names,z_list))
                sort_final = dict(sorted(unsorted.items(), key=lambda x:x[1]))
                
                return jsonify(sort_final)
            except Exception as e:
                    print("Sortin error:", str(e))  # Log the error
                    return {
                        "message": "Something went wrong during matching.",
                        "error": str(e),
                        "data": None
                    }, 500


                
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    api.add_resource(_Edit, '/edit')
    api.add_resource(_Prediction, '/prediction')