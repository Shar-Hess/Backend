from flask import Blueprint, request
from controllers import product_controller

product = Blueprint('product', __name__)

@product.route('/product', methods=["POST"])
def product_add():
    return product_controller.product_add()

@product.route('/product/category', methods=["POST"])
def product_add_category():
    post_data = request.form if request.form else request.json
    product_id = post_data.get('product_id')
    category_id = post_data.get('category_id')
    return product_controller.product_add_category(product_id, category_id)

@product.route('/products', methods=["GET"])
def products_get_all():
    return product_controller.products_get_all()

@product.route('/products/active', methods=["GET"])
def products_get_active():
    return product_controller.products_get_active()

@product.route('/product/<product_id>', methods=["GET"])
def product_get_by_id(product_id):
    return product_controller.product_get_by_id(product_id)

@product.route('/product/company/<company_id>', methods=["GET"])
def products_get_by_company_id(company_id):
    return product_controller.products_get_by_company_id(company_id)

@product.route('/product/<product_id>', methods=["PUT"])
def product_update_by_id(product_id):
    return product_controller.product_update_by_id(product_id)

@product.route('/product/categories/<product_id>', methods=["POST"])
def product_add_category_to_product(product_id):
    post_data = request.form if request.form else request.json
    category_id = post_data.get('category_id')
    return product_controller.product_add_category(product_id, category_id)

@product.route('/product/delete/<product_id>', methods=["DELETE"])
def product_delete_by_id(product_id):
    return product_controller.product_delete_by_id(product_id)