from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from datetime import datetime

from db import db
from models.workout import Workout, workout_schema, workouts_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth, validate_uuid4


def create_workout():
    post_data = request.form if request.form else request.json    

    workout = Workout.new_workout_obj()
    populate_object(workout, post_data)
    
    db.session.add(workout)
    db.session.commit()
    return jsonify({"message": "Workout added", "result": workout_schema.dump(workout)}), 201


@authenticate_return_auth
def get_workout(workout_id, auth_info):
    workout = db.session.query(Workout).filter(Workout.workout_id == workout_id).first()
 
    return jsonify({"message": "Workout found", "result": workout_schema.dump(workout)}), 200

@authenticate_return_auth
def update_workout(workout_id, auth_info):

    workout = db.session.query(Workout).filter(Workout.workout_id == workout_id).first()
  
    populate_object(workout, request.json)

    db.session.commit()
    return jsonify({"message": "Workout updated", "result": workout_schema.dump(workout)}), 200


@authenticate_return_auth
def delete_workout(workout_id, auth_info):

    workout = db.session.query(Workout).filter(Workout.workout_id == workout_id).first()
   
    db.session.delete(workout)
    db.session.commit()
    return jsonify({"message": "Workout deleted"}), 200
