import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float
import marshmallow as ma
from db import db


class UserProfile(db.Model):
    __tablename__ = "UserProfile"

    profile_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('Users.user_id'), nullable=False)
    height = db.Column(Float, nullable=True) 
    weight = db.Column(Float, nullable=True)
    goal_weight_lifted = db.Column(Float, nullable=False)
    

    def __init__(self, height, weight, goal_weight_lifted):
        self.height = height
        self.weight = weight
        self.goal_weight_lifted = goal_weight_lifted

    def new_user_profile_obj():
        return UserProfile( height=None, weight=None, goal_weight_lifted=None)

class UserProfileSchema(ma.Schema):
    class Meta:
        fields = ["user_id", "height", "weight", "goal_weight_lifted"]

user_profile_schema = UserProfileSchema()
