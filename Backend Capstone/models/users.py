import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Date
from db import db  
from flask_bcrypt import generate_password_hash 
import marshmallow as ma

from .user_exercise_xref import user_exercise_xref


class Users(db.Model):
    __tablename__ = "Users" 

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(String(100), nullable=False, unique=True)
    password = db.Column(String(128), nullable=False) 
    join_date = db.Column(Date, nullable=False)
    role = db.Column(String(20), nullable=False, default='user') 

    workouts = db.relationship('Workout', backref='user', lazy=True)
    profile = db.relationship('UserProfile', backref='user', uselist=False, lazy=True)
    
    favorite_exercises = db.relationship('ExerciseType', secondary=user_exercise_xref, back_populates='users')

    def __init__(self, first_name, last_name, email, password, join_date, role='user'):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.join_date = join_date
        self.role = role  

    def new_user_obj():
        return Users(first_name=None, last_name=None, email=None, password=None, join_date=None, role='user')

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'first_name','last_name', 'email', 'join_date', 'role')  

    workouts = ma.fields.Nested('WorkoutSchema', many=True, exclude=('user',))
    profile = ma.fields.Nested('UserProfileSchema', exclude=('user',))
    favorite_exercises = ma.fields.Nested('ExerciseTypeSchema', many=True)

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)