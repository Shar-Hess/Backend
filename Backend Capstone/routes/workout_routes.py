from flask import Blueprint, request
import controllers

workouts = Blueprint('workouts', __name__)

@workouts.route('/workout', methods=['POST'])
def create_workout():
    return controllers.create_workout()

@workouts.route('/workout/<workout_id>', methods=['GET'])
def get_workout(workout_id):
    return controllers.get_workout(workout_id)

@workouts.route('/workout/<workout_id>', methods=['PUT'])
def update_workout(workout_id):
    return controllers.update_workout(workout_id)

@workouts.route('/workout/<workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    return controllers.delete_workout(workout_id)