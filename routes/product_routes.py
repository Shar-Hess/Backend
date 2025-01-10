from flask import Blueprint
import controllers

product = Blueprint('product', __name__)

@product.route('/product', methods=['POST'])
def create_product():
    return controllers.create_product()

@product.route('/products', methods=['GET'])
def read_products():
    return controllers.read_products()

@product.route('/products/active', methods=['GET'])
def read_active_products():
    return controllers.read_active_products()

@product.route('/product/<product_id>', methods=['GET'])
def read_product_by_id(product_id):
    return controllers.read_product_by_id(product_id)


@product.route('/product/<product_id>', methods=['PUT'])
def update_product_by_id(product_id):
    return controllers.update_product_by_id(product_id)

@product.route('/product/activity/<product_id>', methods=['PATCH'])
def toggle_product_activity(product_id):
    return controllers.toggle_product_activity(product_id)

@product.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product_by_id(product_id):
    return controllers.delete_product_by_id(product_id)