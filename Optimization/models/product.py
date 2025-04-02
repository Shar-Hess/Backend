import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from db import db
from models.product_catorgies_xref import products_categories_xref

class Products(db.Model):
    __tablename__ = "Products"

    product_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Companies.company_id"), nullable=False)
    product_name = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float())
    active = db.Column(db.Boolean(), default=True)

    company = db.relationship("Companies", back_populates='products')
    categories = db.relationship(
        "Categories",
        secondary="ProductsCategoriesXref",
        back_populates="products"
    )
    warranties = db.relationship(
        "Warranties",
        foreign_keys='[Warranties.product_id]',
        back_populates='product',
        cascade='all, delete-orphan'  
    )

    def __init__(self, product_name, description, price, company_id, active=True):
        self.product_name = product_name
        self.description = description
        self.price = price
        self.company_id = company_id
        self.active = active

    @staticmethod
    def new_product_obj():
        return Products("", "", None, None, True)

class ProductsSchema(ma.Schema):
    class Meta:
        fields = ['product_id', 'product_name', 'description', 'price', 'company', 'active', 'categories', 'warranties']

    company = ma.fields.Nested("CompaniesSchema", exclude=['products'])
    warranties = ma.fields.Nested("WarrantiesSchema", many=True, exclude=["product"]) 
    categories = ma.fields.Nested("CategoriesSchema", many=True, exclude=["products"])

product_schema = ProductsSchema()
products_schema = ProductsSchema(many=True)