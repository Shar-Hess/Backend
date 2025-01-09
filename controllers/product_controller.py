from flask import jsonify, request
from data import product_records

def update_product(product_id):
    post_data = request.form if request.form else request.json

    product = {}
    product['product_id'] = post_data.get('product_id')

    for record in product_records:
        if record['product_id'] == int(product_id):
            product = record


    product['name'] = post_data.get('name', product['name'])
    product['description'] = post_data.get('description', product['description'])
    product['price'] = post_data.get('price', product['price'])

    product_records.append(product)
    return jsonify({"message": f"Product {product['name']} has been updated."}), 200


def create_product():
    post_data = request.form if request.form else request.json
    product = {}
    product['product_id'] = post_data['product_id']
    product['name'] = post_data['name']
    product['description'] = post_data['description']
    product['price'] = post_data['price']
    product['active'] = post_data['active']
    product_records.append(product)

    return jsonify({"message": f"Product {product['name']} has been added."}), 201

def get_product_by_id(product_id):
    for product in product_records:
        if product['product_id'] == int(product_id):
            return jsonify(product), 200
    return jsonify({"message": f'Product with id {product_id} not found.'}), 404
