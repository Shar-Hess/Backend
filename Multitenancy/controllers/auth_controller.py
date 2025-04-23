from flask import jsonify, request
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta

from db import db
from models.auth_tokens import AuthTokens, auth_token_schema
from models.app_users import AppUsers


def auth_token_add():
    post_data = request.form if request.form else request.json

    email = post_data.get('email')
    password = post_data.get('password')

    if not email or not password:
        return jsonify({'message': 'invalid login'}), 401
    
    now_datetime = datetime.now()
    expiration_datetime = now_datetime + timedelta(hours=12)

    user_query = db.session.query(AppUsers).filter(AppUsers.email == email).first()

    if user_query:
        user_id = user_query.user_id
        is_password_valid = check_password_hash(user_query.password, password)

        if is_password_valid == False:
            return jsonify({'message': 'invalid password'}), 401
        
        existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_id).all()

        if existing_tokens:
            for token in existing_tokens:
                if token.expiration < now_datetime:
                    db.session.delete(token)
        
        new_token = AuthTokens(user_id, expiration_datetime)

        db.session.add(new_token)
        db.session.commit()

        return jsonify({"message": "auth success", "auth_info": auth_token_schema.dump(new_token)}), 201