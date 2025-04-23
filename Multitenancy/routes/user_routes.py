from flask import Blueprint, request

import controllers

users = Blueprint('users', __name__)

@users.route('/user', methods=['POST'])
def add_user():
    return controllers.add_user()

@users.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return controllers.get_user_by_id(request, user_id)

@users.route('/users', methods=['GET'])
def get_all_users():
    return controllers.get_all_users(request)