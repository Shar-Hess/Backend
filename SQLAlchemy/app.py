from flask import Flask, jsonify, request
import psycopg2
import os

from db import init_db, db
from models.categories import Categories
from models.companies import Companies
from models.products import Products
from models.warranties import Warranties
from models.products_categories_xref import products_categories_association_table
import routes

flask_host = os.environ.get("FLASK_HOST")
flask_port = os.environ.get("FLASK_POST")

database_scheme = os.environ.get("DATABASE_SCHEME")
database_user = os.environ.get("DATABASE_USER")
database_address = os.environ.get("DATABASE_ADDRESS")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_scheme}{database_user}@{database_address}:{database_port}/{database_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

init_db(app, db)

app.register_blueprint(routes.company)
app.register_blueprint(routes.product)
app.register_blueprint(routes.category)
app.register_blueprint(routes.warranty)

def create_tables():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("Tables Created")



if __name__ == '__main__':
    create_tables()
    app.run(host=flask_host, port=flask_port)