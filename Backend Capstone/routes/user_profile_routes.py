from flask import Blueprint, request
import controllers

user_profiles = Blueprint('user_profiles', __name__)


@user_profiles.route('/userprofile', methods=['POST'])
def create_user_profile():
    return controllers.create_user_profile()

@user_profiles.route('/userprofile/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    return controllers.get_user_profile( user_id)

@user_profiles.route('/userprofile/<user_id>', methods=['PUT'])
def update_user_profile(user_id):
    return controllers.update_user_profile(user_id)

@user_profiles.route('/userprofile/delete/<user_id>', methods=['DELETE'])
def delete_user_profile(user_id):
    return controllers.delete_user_profile( user_id)