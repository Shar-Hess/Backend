from flask import jsonify, request
from db import db
from models.product import Products, products_schema, product_schema
from models.category import Categories, categories_schema, category_schema
from util.reflection import populate_object

def product_add():
    post_data = request.form if request.form else request.json

    new_product = Products.new_product_obj()
    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "product added", "result": product_schema.dump(new_product)}), 201

def products_get_all():
    products = db.session.query(Products).all()

    if not products:
        return jsonify({"message": "no products found"}), 404

    return jsonify({"message": "products found", "results": products_schema.dump(products)}), 200

def product_get_by_id(product_id):
    product = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product:
        return jsonify({"message": "product not found"}), 404

    return jsonify({"message": "product found", "result": product_schema.dump(product)}), 200

def product_add_category(product_id, category_id):
    product = db.session.query(Products).filter(Products.product_id == product_id).first()
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not product or not category:
        return jsonify({"message": "product or category not found"}), 404

    if category in product.categories:
        return jsonify({"message": "category already associated with this product"}), 400

    product.categories.append(category)
    db.session.commit()
    return jsonify({"message": "category added to product", "result": product_schema.dump(product)}), 200

def products_get_active():
    products = db.session.query(Products).filter(Products.active == True).all()

    if not products:
        return jsonify({"message": "no active products found"}), 404

    return jsonify({"message": "active products found", "results": products_schema.dump(products)}), 200

def products_get_by_company_id(company_id):
    products = db.session.query(Products).filter(Products.company_id == company_id).all()

    if not products:
        return jsonify({"message": "no products found for this company"}), 404

    return jsonify({"message": "products found", "results": products_schema.dump(products)}), 200

def product_update_by_id(product_id):
    post_data = request.form if request.form else request.json

    product = db.session.query(Products).filter(Products.product_id == product_id).first()

    if product:
        populate_object(product, post_data)

        db.session.commit()
        return jsonify({"message": "product updated", "result": product_schema.dump(product)}), 200

    return jsonify({"message": "product not found"}), 404

def product_delete_by_id(product_id):
    product = db.session.query(Products).filter(Products.product_id == product_id).first()

    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "product deleted"}), 200

    return jsonify({"message": "product not found"}), 404