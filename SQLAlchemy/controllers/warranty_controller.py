from flask import jsonify, request

from db import db
from models.warranties import Warranties

def add_warranty():
    post_data = request.form if request.form else request.json

    fields = ['product_id', 'warranty_months']
    required_fields = ['product_id', 'warranty_months']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if  field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data
        
    new_warranty = Warranties(values['product_id'], values ['warranty_months'])

    db.session.add(new_warranty)
    db.session.commit()

    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_months == values['warranty_months']).first()

    warranty = {
        "warranty_id": warranty_query.warranty_id,
        'product_id': warranty_query.product_id,
        "warranty_months": warranty_query.warranty_months
    }

    return jsonify({"message": "warranty created", "results": warranty}), 201


def get_all_warranties():
    warranties_query = db.session.query(Warranties).all()

    warranty_list = []

    for warranty in warranties_query:
        warranty_dict = {
            'warranty_id': warranty.warranty_id,
            'product_id': warranty.product_id,
            'warranty_name': warranty.warranty_months,
        }

        warranty_list.append(warranty_dict)

    return jsonify({"message": "products found", "results": warranty_list}), 200

def get_warranty_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": "warranty does not exist"}), 400
    
    warranty = {
        'warranty_id': warranty_query.warranty_id,
        'warranty_months, ': warranty_query.warranty_months, 
    }

    return jsonify({"message": " warranty found", "results": warranty}), 200


def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.json

    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()
    
    warranty_query.warranty_months = post_data.get('warranty_months', 'warranty_query.warranty_months')

    db.session.commit()

    updated_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    warranty_dict = {
        'warranty_id': updated_query.warranty_id,
        'warranty_months': updated_query.warranty_months,
    }

    return jsonify({"message": "warranty updated", "results": warranty_dict}), 200


def delete_warranty_by_id(warranty_id):
    warranty_query = db.session.query(Warranties).filter(Warranties.warranty_id == warranty_id).first()

    if not warranty_query:
        return jsonify({"message": f"Product by id {warranty_id} does not exist"}), 400    

    try:
        db.session.delete(warranty_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "warranty deleted"}), 200