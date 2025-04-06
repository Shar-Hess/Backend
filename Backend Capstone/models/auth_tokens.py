import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  ForeignKey

from db import db


class AuthTokens(db.Model):
    __tablename__ ="AuthTokens"

    auth_token = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    expiration = db.Column(db.DateTime(), nullable=False)

    user = db.relationship('Users', backref='auth_tokens', lazy=True)

    def __init__(self, user_id, exipration):
        self.user_id = user_id
        self.expiration = exipration
    

class AuthTokensSchema(ma.Schema):
    
    class Meta:
        fields = ['auth_token', 'user', 'expiration']

    user = ma.fields.Nested('UsersSchema', only=['user_id', 'first_name', 'last_name'])


auth_token_schema = AuthTokensSchema()

