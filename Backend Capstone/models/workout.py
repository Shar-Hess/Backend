import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Date, ForeignKey, Float
from db import db
import marshmallow as ma

class Workout(db.Model):
    __tablename__ = 'Workout'

    workout_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('Users.user_id'), nullable=False)
    workout_date = db.Column(Date, nullable=False)
    total_weight_lifted = db.Column(Float, nullable=False)
    
    exercises = db.relationship('Exercise', backref='workout', lazy=True)

    def __init__(self, user_id, workout_date, total_weight_lifted):
        self.user_id = user_id
        self.workout_date = workout_date
        self.total_weight_lifted = total_weight_lifted

    def new_workout_obj():
        return Workout(user_id=None, workout_date=None, total_weight_lifted=None)

class WorkoutSchema(ma.Schema):
    class Meta:
        fields = ('workout_id', 'user_id', 'workout_date', 'total_weight_lifted', 'exercises')

    exercises = ma.fields.Nested('ExerciseSchema', many=True, exclude=('workout',))  


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)