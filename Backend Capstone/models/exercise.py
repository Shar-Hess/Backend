import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from db import db
import marshmallow as ma

class Exercise(db.Model):
    __tablename__ = 'Exercise'

    exercise_id = db.Column(Integer, primary_key=True, autoincrement=True)  
    workout_id = db.Column(UUID(as_uuid=True), ForeignKey('Workout.workout_id'), default=uuid.uuid4)
    exercise_name = db.Column(String(50), nullable=False)
    weight_lifted = db.Column(Float, nullable=False)
    reps = db.Column(Integer, nullable=False)
    sets = db.Column(Integer, nullable=False)

    def __init__(self, exercise_id, exercise_name, weight_lifted, reps, sets):
        self.exercise_id = exercise_id
        self.exercise_name = exercise_name
        self.weight_lifted = weight_lifted
        self.reps = reps
        self.sets = sets


    def new_exercise_obj():
        return Exercise(exercise_id=None, exercise_name=None, weight_lifted=None, reps=None, sets=None)

class ExerciseSchema(ma.Schema):
    class Meta:
      
        fields = ('exercise_id', 'exercise_name', 'weight_lifted', 'reps', 'sets','workout')

    workout = ma.fields.Nested('WorkoutSchema', exclude=('exercises',), default=None)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)