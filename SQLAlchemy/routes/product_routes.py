from flask import Blueprint

import controllers

product = Blueprint('product', __name__)

@product.route('/product', methods=['POST'])
def add_product():
    return controllers.add_product()

@product.route('/product/<product_id>', methods=['GET'])
def get_product_by_id(product_id):
    return controllers.get_product_by_id(product_id)

@product.route('/products', methods=['GET'])
def get_all_products():
    return controllers.get_all_products()

@product.route('/product/category', methods=['POST'])
def product_category_association():
    return controllers.product_category_association()

@product.route('/products', methods=['GET'])
def get_products_by_active():
    return controllers.get_products_by_active()

@product.route('/product/<product_id>', methods=["PUT"])
def update_product_by_id(product_id):
    return controllers.update_product_by_id(product_id) 

@product.route('/product/delete/<product_id>', methods=["DELETE"])
def delete_product_by_id(product_id):
    return controllers.delete_product_by_id(product_id)
