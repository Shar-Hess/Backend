from flask import jsonify, request

from db import db
from models.categories import Categories

def add_category():
    post_data = request.form if request.form else request.json

    fields = ['category_name']
    required_fields = ['category_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if  field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data
        
    new_category = Categories(values['category_name'])

    db.session.add(new_category)
    db.session.commit()

    category_query = db.session.query(Categories).filter(Categories.category_name == values['category_name']).first()

    category = {
        "category_id": category_query.category_id,
        "category_name": category_query.category_name
    }

    return jsonify({"message": "category created", "results": category}), 201

def get_all_categories():
    categories_query = db.session.query(Categories).all()

    category_list = []

    for category in categories_query:
        categories_dict = {
            'categories_id': category.category_id,
            'categories_name': category.category_name,
        }

        category_list.append(categories_dict)

    return jsonify({"message": "categories found", "results": category_list}), 200

def get_category_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": "category does not exist"}), 400
    
    category = {
        'category_id': category_query.category_id,
        'category_name': category_query.category_name
    }

    return jsonify({"message": " category found", "results": category}), 200

def update_category_by_id(category_id):
    post_data = request.form if request.form else request.json

    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()
    
    category_query.category_name = post_data.get('category_name', 'category_query.category_name')

    db.session.commit()

    updated_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    category_dict = {
        'category_id': updated_query.category_id,
        'category_name': updated_query.category_name,
    }

    return jsonify({"message": "category updated", "results": category_dict}), 200


def delete_category_by_id(category_id):
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category_query:
        return jsonify({"message": f"Category by id {category_id} does not exist"}), 400    

    try:
        db.session.delete(category_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "category deleted"}), 200