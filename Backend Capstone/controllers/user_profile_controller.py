from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from datetime import datetime

from db import db
from models.user_profile import UserProfile, user_profile_schema

from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth, validate_uuid4


def create_user_profile():
    post_data = request.form if request.form else request.json

    profile = UserProfile.new_user_profile_obj() 
    populate_object(profile, post_data)

    db.session.add(profile)
    db.session.commit()
    return jsonify({"message": "Profile added", "result": user_profile_schema.dump(profile)}), 201

# @authenticate_return_auth
def get_user_profile(user_id):

    profile = db.session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
   
    return jsonify({"message": "Profile found", "result": user_profile_schema.dump(profile)}), 200

# @authenticate_return_auth
def update_user_profile(user_id):
   
    profile = db.session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        return jsonify({"message": "Profile not found"}), 404

    populate_object(profile, request.json)

    db.session.commit()
    return jsonify({"message": "Profile updated", "result": user_profile_schema.dump(profile)}), 200


def delete_user_profile(user_id):

    profile = db.session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        return jsonify({"message": "Profile not found"}), 404


    db.session.delete(profile)
    db.session.commit()
    return jsonify({"message": "Profile deleted"}), 200

