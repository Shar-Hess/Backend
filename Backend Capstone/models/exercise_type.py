import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String
from db import db
import marshmallow as ma
from .user_exercise_xref import user_exercise_xref


class ExerciseType(db.Model):
    __tablename__ = 'ExerciseType'

    exercise_type_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_name = db.Column(String(50), nullable=False, unique=True)
    muscle_group = db.Column(String(50), nullable=False)

    users = db.relationship('Users', secondary=user_exercise_xref, back_populates='favorite_exercises')

    def __init__(self, type_name, muscle_group):
        self.type_name = type_name
        self.muscle_group = muscle_group

    @staticmethod
    def new_exercise_type_obj():
        return ExerciseType(type_name=None, muscle_group=None)

class ExerciseTypeSchema(ma.Schema):
    class Meta:
        fields = ('exercise_type_id', 'type_name', 'muscle_group')  

    users = ma.fields.Nested('UsersSchema', many=True, exclude=('favorite_exercises',))

exercise_type_schema = ExerciseTypeSchema()
exercise_types_schema = ExerciseTypeSchema(many=True)