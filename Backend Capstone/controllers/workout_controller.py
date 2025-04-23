from flask import jsonify, request
from datetime import datetime

from db import db
from models.workout import Workout, workout_schema, workouts_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth, validate_uuid4

@authenticate_return_auth
def create_workout(auth_info):
    try:
        post_data = request.form if request.form else request.json    
        
        # Add validation for required fields
        required_fields = ['workout_name', 'date']  # Add any other required fields
        for field in required_fields:
            if field not in post_data:
                return jsonify({"message": f"Missing required field: {field}"}), 400

        workout = Workout.new_workout_obj()
        populate_object(workout, post_data)
        
        db.session.add(workout)
        db.session.commit()
        return jsonify({
            "message": "Workout added", 
            "result": workout_schema.dump(workout)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating workout: {str(e)}"}), 500

@authenticate_return_auth
def get_workout(workout_id, auth_info):
    try:
        workout = db.session.query(Workout).filter(Workout.workout_id == workout_id).first()
        if not workout:
            return jsonify({"message": "Workout not found"}), 404
     
        return jsonify({
            "message": "Workout found", 
            "result": workout_schema.dump(workout)
        }), 200
    except Exception as e:
        return jsonify({"message": f"Error fetching workout: {str(e)}"}), 500

@authenticate_return_auth
def update_workout(workout_id, auth_info):
    try:
        workout = db.session.query(Workout).filter(Workout.workout_id == workout_id).first()
        if not workout:
            return jsonify({"message": "Workout not found"}), 404

        post_data = request.form if request.form else request.json
        populate_object(workout, post_data)

        db.session.commit()
        return jsonify({
            "message": "Workout updated", 
            "result": workout_schema.dump(workout)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating workout: {str(e)}"}), 500

@authenticate_return_auth
def delete_workout(workout_id, auth_info):
    try:
        workout = db.session.query(Workout).filter(Workout.workout_id == workout_id).first()
        if not workout:
            return jsonify({"message": "Workout not found"}), 404
       
        db.session.delete(workout)
        db.session.commit()
        return jsonify({"message": "Workout deleted"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error deleting workout: {str(e)}"}), 500
