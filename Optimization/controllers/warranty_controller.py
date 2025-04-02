from flask import jsonify, request
from db import db
from models.warranty import Warranties, warranties_schema, warranty_schema
from util.reflection import populate_object

def warranty_add():
    post_data = request.form if request.form else request.json

    new_warranty = Warranties.new_warranty_obj()
    populate_object(new_warranty, post_data)

    db.session.add(new_warranty)
    db.session.commit()

    return jsonify({"message": "warranty added", "result": warranty_schema.dump(new_warranty)}), 201

def warranties_get_by_product_id(product_id):
    warranties = db.session.query(Warranties).filter(Warranties.product_id == product_id).all()

    if not warranties:
        return jsonify({"message": "no warranties found for this product"}), 404

    return jsonify({"message": "warranties found", "results": warranties_schema.dump(warranties)}), 200

def warranties_get_all():
    warranties = db.session.query(Warranties).all()

    if not warranties:
        return jsonify({"message": "no warranties found"}), 404

    return jsonify({"message": "warranties found", "results": warranties_schema.dump(warranties)}), 200

def warranty_get_by_id(warranty_id):
    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty:
        return jsonify({"message": "warranty not found"}), 404

    return jsonify({"message": "warranty found", "result": warranty_schema.dump(warranty)}), 200

def warranty_update_by_id(warranty_id):
    post_data = request.form if request.form else request.json

    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if warranty:
        populate_object(warranty, post_data)

        db.session.commit()
        return jsonify({"message": "warranty updated", "result": warranty_schema.dump(warranty)}), 200

    return jsonify({"message": "warranty not found"}), 404

def warranty_delete_by_id(warranty_id):
    warranty = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if warranty:
        db.session.delete(warranty)
        db.session.commit()
        return jsonify({"message": "warranty deleted"}), 200

    return jsonify({"message": "warranty not found"}), 404