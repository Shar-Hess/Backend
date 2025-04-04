from flask import jsonify, request

from db import db 
from models.company import Companies, companies_schema, company_schema
from util.reflection import populate_object

def company_add():
    post_data= request.form if request.form else request.json

    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company added", "result": company_schema.dump(new_company)}), 201


def companies_get_all():
    companies = db.session.query(Companies).all()

    if not companies:
        return jsonify({"message": "no companies found"}), 404

    else:
      return jsonify({"message": "companies found", "results": companies_schema.dump(companies)}), 200

def company_get_by_id(company_id):
    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company:
        return jsonify({"message": "company not found"}), 404

    return jsonify({"message": "company found", "result": company_schema.dump(company)}), 200


def company_update_by_id(company_id):
    post_data = request.form if request.form else request.json

    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if company:
        populate_object(company, post_data)

        db.session.commit()
        return jsonify({"message": "company updated", "results": company_schema.dump(company)}), 200

    return jsonify({"message": "company not found"})

def company_delete_by_id(company_id):
    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if company:
        db.session.delete(company)
        db.session.commit()
        return jsonify({"message": "company deleted"}), 200

    return jsonify({"message": "company not found"}), 404