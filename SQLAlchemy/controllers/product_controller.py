from flask import jsonify, request

from db import db
from models.products import Products
from models.categories import Categories

def add_product():
    post_data = request.form if request.form else request.json

    fields = ['company_id', 'product_name', 'description', 'price']
    required_fields = ['company_id',  'product_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if  field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data
        
    new_product = Products(values['company_id'], values['product_name'], values['description'], values['price'])

    db.session.add(new_product)
    db.session.commit()

    product_query = db.session.query(Products).filter(Products.product_name == values['product_name']).first()

    product = {
        'product_id': product_query.product_id,
        'company_id': product_query.company_id,
        'product_name': product_query.product_name,
        'description': product_query.description,
        'price': product_query.price,
        'active': product_query.active
    }

    return jsonify({"message": "product added", "results": product}), 201


def get_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    if not product_query:
        return jsonify({"message": f"product not found"}), 400

    print(product_query)

    company_dict = {
        'company_id': product_query.company.company_id,
        'company_name': product_query.company.company_name
    }

    if product_query.warranty:
        warranty_dict = {
            'warranty_id': product_query.warranty.warranty_id,
            'warranty_months': product_query.warranty.warranty_months
        }
    else:
        warranty_dict = {}

    categories_list = []

    for category in product_query.categories:
        categories_list.append({
            "category_id": category.category_id,
            "category_name": category.category_name
        })

    product = {
        'product_id': product_query.product_id,
        'product_name': product_query.product_name,
        'description': product_query.description,
        'price': product_query.price,
        'active': product_query.active,
        'company': company_dict,
        'warranty': warranty_dict,
        'categories': categories_list
    }

    return jsonify({"message": "product found", "results": product}), 200


def get_all_products():
    products_query = db.session.query(Products).all()

    product_list = []

    for product in products_query:
        products_dict = {
            'products_id': product.product_id,
            'products_name': product.product_name,
        }

        product_list.append(products_dict)

    return jsonify({"message": "products found", "results": product_list}), 200


def product_category_association():
    post_data = request.form if request.form else request.get_json()

    fields = ['product_id', 'category_id']
    required_fields = ['product_id', 'category_id']

    values = {}

    for field in fields:
        field_data = post_data.get(field)
        if field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400

        values[field] = field_data

    product_query = db.session.query(Products).filter(Products.product_id == values['product_id']).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == values['category_id']).first()

    if product_query and category_query:
        product_query.categories.append(category_query)

        db.session.commit()

        categories_list = []

        for category in product_query.categories:
            categories_list.append({
                "category_id": category.category_id,
                "category_name": category.category_name
            })

        company_dict = {
            "company_id": product_query.company.company_id,
            "company_name": product_query.company.company_name
        }

        product = {
            'product_id': product_query.product_id,
            'product_name': product_query.product_name,
            'description': product_query.description,
            'price': product_query.price,
            'active': product_query.active,
            'company': company_dict,
            'categories': categories_list,
        }

    return jsonify({"message": "category added to product", "result": product}), 201

def get_products_by_active():
    product_query = db.session.query(Products).filter(Products.active == True, ).all()
    if not product_query:
        return jsonify({"message": f"product not found"}), 400
    

    
    return jsonify({"product": product_query.to_dict()}), 200 

def update_product_by_id(product_id):
    post_data = request.form if request.form else request.json

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    
    product_query.product_name = post_data.get('product_name', 'product_query.product_name')

    db.session.commit()

    updated_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    product_dict = {
        'product_id': updated_query.product_id,
        'company_id': updated_query.company_id,
        'product_name': updated_query.product_name,
        'description': updated_query.description,
        'price': updated_query.price,
        'active': updated_query.active,
    }

    return jsonify({"message": "product updated", "results": product_dict}), 200

def delete_product_by_id(product_id):
    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if not product_query:
        return jsonify({"message": f"Product by id {product_id} does not exist"}), 400    

    try:
        db.session.delete(product_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "product deleted"}), 200


