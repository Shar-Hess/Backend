import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class AppUsers(db.Model):
    __tablename__ ="AppUsers"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Organizations.org_id'), nullable=False)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String())
    active = db.Column(db.Boolean(), nullable=False, default=True)
    role = db.Column(db.String(), nullable=False, default='user')


    auth = db.relationship('AuthTokens', back_populates='user')
    org = db.relationship('Organizations', back_populates='users')

    def __init__(self, org_id, first_name, last_name, email, password, phone=None, active=True, role='user'):
        self.org_id = org_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.active = active
        self.role = role

    def new_user_obj():
        return AppUsers(None, None, None, None, None, None, True, 'user')
    

class AppUsersSchema(ma.Schema):
    
    class Meta:
        fields = ['user_id', 'org', 'first_name', 'last_name', 'email', 'phone', 'active', 'role']

    org = ma.fields.Nested('OrganizationsSchema', exclude=['users'])


app_user_schema = AppUsersSchema()
app_users_schema = AppUsersSchema(many=True)
