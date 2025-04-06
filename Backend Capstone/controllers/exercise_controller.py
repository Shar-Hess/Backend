from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from datetime import datetime

from db import db
from models.workout import Workout, workout_schema, workouts_schema
from models.exercise import Exercise, exercise_schema, exercises_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth, validate_uuid4


def create_exercise():
    post_data = request.form if request.form else request.json
    required_fields = ['exercise_name', 'weight_lifted', 'reps', 'sets', 'workout_id']
    for field in required_fields:
        if field not in post_data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
    
    workout_id = post_data['workout_id']

    workout = db.session.query(Workout).filter(Workout.workout_id == post_data['workout_id']).first()
    if not workout:
        return jsonify({"message": "Workout not found or unauthorized"}), 404
    
    exercise = Exercise.new_exercise_obj()
    populate_object(exercise, post_data)

    db.session.add(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise added", "result": exercise_schema.dump(exercise)}), 201


def get_all_exercises(request):
    # if auth_info.user.role != 'trainer':  
    #     return jsonify({"message": "Unauthorized"}), 403

    users_query = db.session.query(Exercise).all()
    return jsonify({"message": "Users found", "result": exercises_schema.dump(users_query)}), 200


def get_exercise_by_id(exercise_id, auth_info):
    exercise_id = request.view_args.get('exercise_id')
    exercise = db.session.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()

    return jsonify({"message": "Exercise found", "result": exercise_schema.dump(exercise)}), 200

def update_exercise(exercise_id, auth_info):
    exercise_id = request.view_args.get('exercise_id')
    exercise = db.session.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()

    populate_object(exercise, request.json)

    db.session.commit()
    return jsonify({"message": "Exercise updated", "result": exercise_schema.dump(exercise)}), 200


def delete_exercise(exercise_id, auth_info):
    exercise_id = request.view_args.get('exercise_id')
    exercise = db.session.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()


    db.session.delete(exercise)
    db.session.commit()
    return jsonify({"message": "Exercise deleted"}), 200
