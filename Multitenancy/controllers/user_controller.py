from flask import jsonify, request
from flask_bcrypt import generate_password_hash

from db import db
from models.app_users import AppUsers, app_user_schema, app_users_schema
from models.organizations import Organizations
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth, validate_uuid4

def add_user():
    post_data = request.form if request.form else request.json
    org_id = post_data.get('org_id')

    new_user = AppUsers.new_user_obj()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

    if org_id:
        if validate_uuid4(org_id) == True:
            org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()

            if org_query == None:
                return jsonify({"message": "org id is required"}), 400
            
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user added", "result": app_user_schema.dump(new_user)}), 201

@authenticate
def get_all_users(request):
    users_query = db.session.query(AppUsers). all()

    return jsonify({"message": "users found", "result": app_users_schema.dump(users_query)}), 200

@authenticate_return_auth
def get_user_by_id(request, user_id, auth_info):
    user_query = db.session.query(AppUsers).filter(AppUsers.user_id == user_id).first()

    if auth_info.user.role == 'super-admin' or user_id == str(auth_info.user.user_id):
        return jsonify({"message": "user found", "result": app_user_schema.dump(user_query)}), 200
    
    else:
        return jsonify({"message": "unauthoried"}), 401
    


