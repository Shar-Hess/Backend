from flask import Blueprint, request
import controllers

exercise_types = Blueprint('exercise_types', __name__)

@exercise_types.route('/exercise_type', methods=['POST'])
def create_exercise_type():
    return controllers.create_exercise_type()

@exercise_types.route('/exercise_type/<exercise_type_id>', methods=['GET'])
def get_exercise_type(exercise_type_id):
    return controllers.get_exercise_type( exercise_type_id)

@exercise_types.route('/exercise_type/<exercise_type_id>', methods=['PUT'])
def update_exercise_type(exercise_type_id):
    return controllers.update_exercise_type(exercise_type_id)

@exercise_types.route('/exercise_type/delete/<exercise_type_id>', methods=['DELETE'])
def delete_exercise_type(exercise_type_id):
    return controllers.delete_exercise_type(exercise_type_id)