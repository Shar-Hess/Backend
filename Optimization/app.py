from flask import Flask, jsonify, request
import psycopg2
import os

from flask_marshmallow import Marshmallow

from db import *
from util.reflection import populate_object

from models.company import Companies, companies_schema, company_schema
from models.product import Products

flask_host = os.environ.get("FLASK_HOST")
flask_port = os.environ.get("FLASK_PORT")

database_scheme = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_scheme}{database_user}@{database_address}:{database_port}/{database_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)

ma = Marshmallow(app)

def create_tables():
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created")


@app.route('/company', methods=["POST"])
def company_add():
    post_data= request.form if request.form else request.json

    new_company = Companies.new_company_obj()
    populate_object(new_company, post_data)

    db.session.add(new_company)
    db.session.commit()

    return jsonify({"message": "company added", "result": company_schema.dump(new_company)}), 201

@app.route('/companies', methods=["GET"])
def companies_get_all():
    companies = db.session.query(Companies).all()

    if not companies:
        return jsonify({"message": "no companies found"}), 404

    else:
      return jsonify({"message": "companies found", "results": companies_schema.dump(companies)}), 200

@app.route('/company/<company_id>', methods=['PUT'])
def company_update_by_id(company_id):
    post_data = request.form if request.form else request.json

    company = db.session.query(Companies).filter(Companies.company_id == company_id).first()

    if company:
        populate_object(company, post_data)

        db.session.commit()
        return jsonify({"message": "company updated", "results": company_schema.dump(company)}), 200

    return jsonify({"message": "company not found"})

if __name__ == '__main__':
    create_tables()
    app.run(host=flask_host, port=flask_port)

