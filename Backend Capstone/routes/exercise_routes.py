from flask import Blueprint, request
import controllers

exercises = Blueprint('exercises', __name__)

@exercises.route('/exercise', methods=['POST'])
def create_exercise():
    return controllers.create_exercise()

@exercises.route('/exercise/<exercise_id>', methods=['GET'])
def get_exercise_by_id(exercise_id):
    return controllers.get_exercise_by_id(request, exercise_id)

@exercises.route('/exercises', methods=['GET'])
def get_all_exercises():
    return controllers.get_all_exercises(request)

@exercises.route('/exercise/<exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    return controllers.update_exercise(request, exercise_id)

@exercises.route('/exercise/<exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    return controllers.delete_exercise(request, exercise_id)