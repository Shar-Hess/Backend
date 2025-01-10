from flask import jsonify, request
from data import product_records

def create_product():
    post_data = request.form if request.form else request.json
    product = {}
    product['product_id'] = post_data['product_id']
    product['name'] = post_data['name']
    product['description'] = post_data['description']
    product['price'] = post_data['price']
    product['active'] = post_data['active']
    product_records.append(product)

    return jsonify({"message": f"product {product['name']} has been added."}), 201

def read_products():
    return jsonify({"message": f'here are all products {product_records}'}), 200

def read_active_products():
    active_products = [product for product in product_records if product["active"]]
    return jsonify({"message": f'here are all active products {active_products}'}), 200

def read_product_by_id(product_id):
    for product in product_records:
        if product["product_id"] == product_id:
            return jsonify(product), 200
    return jsonify({"error": "Product not found"}), 404


def update_product_by_id(product_id):
    post_data = request.form if request.form else request.json

    for product in product_records:
        print(product)
        if product['product_id'] == product_id:
            product["name"] = post_data.get("name", product["name"])
            product["description"] = post_data.get("description", product["description"])
            product["price"] = post_data.get("price", product["price"])
            product["active"] = post_data.get("active", product["active"])  

            return jsonify({"message": f"Product {product['name']} has been updated."}), 200
    
    return jsonify({"error": "Product not found"}), 404


def toggle_product_activity(product_id):
    for product in product_records:
        if product["product_id"] == product_id:
            product["active"] = not product["active"]
            return jsonify({"message": "Product activity toggled", "product": product}), 200
    
    return jsonify({"error": "Product not found"}), 404

def delete_product_by_id(product_id):
    for product in product_records:
        if product["product_id"] == int(product_id):
            product_records.remove(product)

            return jsonify({"message": f"Product with id {product_id} has been deleted."}), 200
    return jsonify({"error": "Product not found"}), 404