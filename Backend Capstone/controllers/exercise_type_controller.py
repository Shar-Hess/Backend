from flask import jsonify, request
from flask_bcrypt import generate_password_hash
from datetime import datetime

from db import db
from models.exercise_type import ExerciseType, exercise_type_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth, validate_uuid4



def create_exercise_type():
    post_data = request.form if request.form else request.json
    exercise_type = ExerciseType.new_exercise_type_obj()
    populate_object(exercise_type, post_data)

    db.session.add(exercise_type)
    db.session.commit()
    return jsonify({"message": "Exercise type added", "result": exercise_type_schema.dump(exercise_type)}), 201



def get_exercise_type(exercise_type_id):

    exercise_type = db.session.query(ExerciseType).filter(ExerciseType.exercise_type_id == exercise_type_id).first()
  
    return jsonify({"message": "Exercise type found", "result": exercise_type_schema.dump(exercise_type)}), 200


def update_exercise_type(exercise_type_id):

    exercise_type = db.session.query(ExerciseType).filter(ExerciseType.exercise_type_id == exercise_type_id).first()
    if not exercise_type:
        return jsonify({"message": "Exercise type not found"}), 404

    populate_object(exercise_type, request.json)

    db.session.commit()
    return jsonify({"message": "Exercise type updated", "result": exercise_type_schema.dump(exercise_type)}), 200

def delete_exercise_type(exercise_type_id):
    exercise_type = db.session.query(ExerciseType).filter(ExerciseType.exercise_type_id == exercise_type_id).first()
    if not exercise_type:
        return jsonify({"message": "Exercise type not found"}), 404


    db.session.delete(exercise_type)
    db.session.commit()
    return jsonify({"message": "Exercise type deleted"}), 200
