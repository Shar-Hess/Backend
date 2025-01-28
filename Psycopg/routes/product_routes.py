# from flask import Blueprint, request, jsonify

# from controllers import product_controller

# product = Blueprint('product', __name__)

# @product.route('/product', methods=["POST"])
# def create_product(product_name, description, price):
#     post_data = request.form if request.form else request.get_json()
    

#     new_product = product_controller.create_product()
#     return jsonify(new_product), 201
