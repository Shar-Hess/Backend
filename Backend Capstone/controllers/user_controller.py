from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from datetime import datetime

from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth, validate_uuid4

def create_user():
    post_data = request.form if request.form else request.json
    new_user = Users.new_user_obj()

    populate_object(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf8')

    new_user.join_date = datetime.now().date()

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "user added", "result": user_schema.dump(new_user)}), 201

# @authenticate
def get_all_users(request):
    # if auth_info.user.role != 'trainer':  
    #     return jsonify({"message": "Unauthorized"}), 403

    users_query = db.session.query(Users).all()
    return jsonify({"message": "Users found", "result": users_schema.dump(users_query)}), 200

@authenticate_return_auth
def get_user_by_id(request, user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if auth_info.user.role == 'trainer' or user_id == str(auth_info.user.user_id):
        return jsonify({"message": "user found", "result": user_schema.dump(user_query)}), 200
    
    else:
        return jsonify({"message": "unauthoried"}), 401
    
@authenticate_return_auth
def update_user(request, user_id, auth_info):
    post_data = request.form if request.form else request.json
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if auth_info.user.role != 'trainer' and str(auth_info.user.user_id) != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    populate_object(user, post_data)
    if 'password' in post_data:
        user.password = generate_password_hash(post_data['password']).decode('utf-8')

    try:
        db.session.commit()
        return jsonify({"message": "User updated", "result": user_schema.dump(user)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error: {str(e)}"}), 500
    


def user_delete_by_id(request, user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "user deleted"}), 200

    return jsonify({"message": "user not found"}), 404