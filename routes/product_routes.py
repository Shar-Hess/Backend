from flask import Blueprint
import controllers

product = Blueprint('product', __name__)

@product.route('/product/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    return controllers.get_product_by_id(product_id)

@product.route('/product', methods=['POST'])
def create_product():
    return controllers.create_product(product_id)

@product.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    return controllers.update_product(product_id)