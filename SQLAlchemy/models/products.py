import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from models.products_categories_xref import products_categories_association_table

class Products(db.Model):
    __tablename__ = "Products"
    
    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Companies.company_id'), nullable=False)
    product_name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())
    price = db.Column(db.Float())
    active = db.Column(db.Boolean())

    company = db.relationship('Companies',foreign_keys='[Products.company_id]', back_populates='products')
    categories = db.relationship('Categories', secondary=products_categories_association_table, back_populates='products')
    warranty = db.relationship('Warranties', foreign_keys='[Warranties.product_id]', back_populates='product', uselist=False, cascade='all')


    def __init__(self, company_id, product_name, description=None, price=None, active=True ):
        self.company_id = company_id
        self.product_name = product_name
        self.description = description
        self.price = price
        self.active = active

