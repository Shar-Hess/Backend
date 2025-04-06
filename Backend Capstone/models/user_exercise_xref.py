import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from sqlalchemy import  ForeignKey

from db import db

user_exercise_xref = db.Table(
    "UserExerciseXref",
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("Users.user_id"), primary_key=True),
    db.Column("exercise_type_id", UUID(as_uuid=True), db.ForeignKey("ExerciseType.exercise_type_id"), primary_key=True)
)