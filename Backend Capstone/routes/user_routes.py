from flask import Blueprint, request
import controllers

users = Blueprint('users', __name__)

@users.route('/user', methods=['POST'])
def create_user():
    return controllers.create_user()

@users.route('/user/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    return controllers.get_user_by_id(request, user_id)

@users.route('/users', methods=['GET'])
def get_all_users():
    return controllers.get_all_users(request)

@users.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    return controllers.update_user(request, user_id)

@users.route('/user/delete/<user_id>', methods=['DELETE'])
def user_delete_by_id(user_id):
    return controllers.user_delete_by_id(request, user_id)
