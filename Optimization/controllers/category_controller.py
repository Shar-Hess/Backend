from flask import jsonify, request
from db import db
from models.category import Categories, categories_schema, category_schema
from util.reflection import populate_object


def category_add():
    post_data = request.form if request.form else request.json

    new_category = Categories.new_category_obj()
    populate_object(new_category, post_data)

    db.session.add(new_category)
    db.session.commit()

    return jsonify({"message": "category added", "result": category_schema.dump(new_category)}), 201

def categories_get_all():
    categories = db.session.query(Categories).all()

    if not categories:
        return jsonify({"message": "no categories found"}), 404

    return jsonify({"message": "categories found", "results": categories_schema.dump(categories)}), 200

def category_get_by_id(category_id):
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if not category:
        return jsonify({"message": "category not found"}), 404

    return jsonify({"message": "category found", "result": category_schema.dump(category)}), 200

def category_update_by_id(category_id):
    post_data = request.form if request.form else request.json

    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if category:
        populate_object(category, post_data)

        db.session.commit()
        return jsonify({"message": "category updated", "result": category_schema.dump(category)}), 200

    return jsonify({"message": "category not found"}), 404

# DELETE
def category_delete_by_id(category_id):
    category = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if category:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": "category deleted"}), 200

    return jsonify({"message": "category not found"}), 404