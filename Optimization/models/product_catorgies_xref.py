
import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

products_categories_xref = db.Table(
    "ProductsCategoriesXref",
    db.Column("product_id", UUID(as_uuid=True), db.ForeignKey("Products.product_id"), primary_key=True),
    db.Column("category_id", UUID(as_uuid=True), db.ForeignKey("Categories.category_id"), primary_key=True)
)