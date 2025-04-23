from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from datetime import datetime

from db import db
from models.workout import Workout, workout_schema, workouts_schema
from models.exercise import Exercise, exercise_schema, exercises_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth, validate_uuid4

@authenticate_return_auth
def create_exercise(auth_info):
    post_data = request.form if request.form else request.json
    required_fields = ['exercise_name', 'weight_lifted', 'reps', 'sets', 'workout_id']
    for field in required_fields:
        if field not in post_data:
            return jsonify({"message": f"Missing required field: {field}"}), 400
    
    workout_id = post_data['workout_id']
    workout = db.session.query(Workout).filter(Workout.workout_id == workout_id).first()
    
    if not workout:
        return jsonify({"message": "Workout not found"}), 404
    
    exercise = Exercise.new_exercise_obj()
    populate_object(exercise, post_data)

    try:
        db.session.add(exercise)
        db.session.commit()
        return jsonify({"message": "Exercise added", "result": exercise_schema.dump(exercise)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating exercise: {str(e)}"}), 500

@authenticate_return_auth
def get_all_exercises(auth_info):
    try:
        exercises_query = db.session.query(Exercise).all()
        return jsonify({
            "message": "Exercises found", 
            "result": exercises_schema.dump(exercises_query)
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching exercises: {str(e)}"}), 500

@authenticate_return_auth
def get_exercise_by_id(exercise_id, auth_info):
    try:
        exercise = db.session.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()
        if not exercise:
            return jsonify({"message": "Exercise not found"}), 404
            
        return jsonify({
            "message": "Exercise found", 
            "result": exercise_schema.dump(exercise)
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching exercise: {str(e)}"}), 500

@authenticate_return_auth
def update_exercise(exercise_id, auth_info):
    try:
        exercise = db.session.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()
        if not exercise:
            return jsonify({"message": "Exercise not found"}), 404

        post_data = request.form if request.form else request.json
        populate_object(exercise, post_data)

        db.session.commit()
        return jsonify({
            "message": "Exercise updated", 
            "result": exercise_schema.dump(exercise)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating exercise: {str(e)}"}), 500

@authenticate_return_auth
def delete_exercise(exercise_id, auth_info):
    try:
        exercise = db.session.query(Exercise).filter(Exercise.exercise_id == exercise_id).first()
        if not exercise:
            return jsonify({"message": "Exercise not found"}), 404

        db.session.delete(exercise)
        db.session.commit()
        return jsonify({"message": "Exercise deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting exercise: {str(e)}"}), 500
