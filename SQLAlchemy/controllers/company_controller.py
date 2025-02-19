from flask import jsonify, request

from db import db
from models.companies import Companies
from models.products import Products

def add_company():
    post_data = request.form if request.form else request.json

    fields = ['company_name']
    required_fields = ['company_name']

    values = {}

    for field in fields:
        field_data = post_data.get(field)

        if  field_data in required_fields and not field_data:
            return jsonify({"message": f'{field} is required'}), 400
        
        values[field] = field_data
        
    new_company = Companies(values['company_name'])

    db.session.add(new_company)
    db.session.commit()

    company_query = db.session.query(Companies).filter(Companies.company_name == values['company_name']).first()

    company = {
        "company_id": company_query.company_id,
        "company_name": company_query.company_name
    }

    return jsonify({"message": "company created", "results": company}), 201

def get_all_companies():
    companies_query = db.session.query(Companies).all()

    company_list = []

    for company in companies_query:
        company_dict = {
            'company_id': company.company_id,
            'company_name': company.company_name,
        }

        company_list.append(company_dict)

    return jsonify({"message": "companies found", "results": company_list}), 200

def get_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    if not company_query:
        return jsonify({"message": f"company does not exist"}), 400

    company = {
        'company_id': company_query.company_id,
        'company_name': company_query.company_name,
    }

    return jsonify({"message": "company found", "results": company}), 200

def update_company_by_id(company_id):
    post_data = request.form if request.form else request.json

    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()
    
    company_query.company_name = post_data.get('company_name', 'company_query.company_name')

    db.session.commit()

    updated_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    company_dict = {
        'company_id': updated_query.company_id,
        'company_name': updated_query.company_name,
    }

    return jsonify({"message": "company updated", "results": company_dict}), 200

def delete_company_by_id(company_id):
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": f"Product by id {company_id} does not exist"}), 400    

    try:
        db.session.delete(company_query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "company deleted"}), 200

def product_company_association(company_id):
 
    company_query = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if not company_query:
        return jsonify({"message": "Company not found"}), 404


    products_list = []

    for product in company_query.products:
        products_list.append({
            "product_id": product.product_id,
            "product_name": product.product_name
        })


    company_dict = {
        "company_id": company_query.company_id,
        "company_name": company_query.company_name
    }

    product = {
        'company': company_dict,
        'products': products_list

    }

    return jsonify({"message": "products", "result": product}), 201


