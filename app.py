from flask import Flask
import routes

app = Flask(__name__)

app.register_blueprint(routes.product)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8086')

# @app.route('/return-body', methods=['POST'])
# def return_body():
#     post_data = request.form if request.form else request.json
#     return jsonify({"message": f'hello, {post_data["first_name"]} {post_data["last_name"]}, you currently have an active status of {post_data["active"]} in our program with a grade of {post_data["grade"]}'}), 200

# @app.route('/route-name')
# def function_name():
#     sum = 3+4

#     return sum

# @app.route('/string')
# def respond_string():
#     return 'Here is a response with a python string'

# @app.route('/html')
# def respond_html():
#     return '<h1 align="center" style="color: blue;">Here is a response with HTML</h1>'

# @app.route('/json')
# def respond_json():
#     return jsonify('Here is a response with json')

# @app.route('/json')
# def respond_json():
#     def addition():
#         count = 9 + 11
#         return count
#     sum = addition()
#     return jsonify({"message": f'Here is a response with text and another return {sum}'})

# @app.route('/json/<number>')
# def respond_json(number):
#     return jsonify({"message": f'Here is a response with the sent slug {number}'})


# product_records = [
#     {
#         "product_id": 1,
#         "name": "Hasbro Gaming Clue Game",
#         "description": "One murder... 6 suspects...",
#         "price": 9.95,
#         "active": True
#     },
#     {
#         "product_id": 2,
#         "name": "Monopoly Board Game The Classic Edition, 2-8 players",
#         "description" : "Relive the Monopoly experiences...", 
#         "price": 35.50,
#         "active": False
#     }
# ]

# @app.route('/product/<product_id>', methods=['PUT'])
# def update_product(product_id):
#     post_data = request.form if request.form else request.json

#     product = {}
#     product['product_id'] = post_data.get('product_id')

#     for record in product_records:
#         if record['product_id'] == int(product_id):
#             product = record


#     product['name'] = post_data.get('name', product['name'])
#     product['description'] = post_data.get('description', product['description'])
#     product['price'] = post_data.get('price', product['price'])

#     product_records.append(product)
#     return jsonify({"message": f"Product {product['name']} has been updated."}), 200


# @app.route('/product', methods=['POST'])
# def create_product():
#     post_data = request.form if request.form else request.json
#     product = {}
#     product['product_id'] = post_data['product_id']
#     product['name'] = post_data['name']
#     product['description'] = post_data['description']
#     product['price'] = post_data['price']
#     product['active'] = post_data['active']
#     product_records.append(product)

#     return jsonify({"message": f"Product {product['name']} has been added."}), 201

# @app.route('/product/<product_id>', methods=['GET'])
# def get_product_by_id(product_id):
#     for product in product_records:
#         if product['product_id'] == int(product_id):
#             return jsonify(product), 200
#     return jsonify({"message": f'Product with id {product_id} not found.'}), 404

# @app.route('/whatsmymethod', methods=["POST"])
# def create_method():
#     return jsonify({"message": "POST: you have created a record"}) , 201
    
# @app.route('/whatsmymethod', methods=["GET"])
# def get_method():
#     return jsonify({"message": "GET: here is your record to read"}), 200

# @app.route('/whatsmymethod', methods=["PUT"])
# def update_method():
#     return jsonify({"message": "PUT: you have setup new values or a record"}), 200


# @app.route('/whatsmymethod', methods=["PATCH"])
# def patch_method():
#     return jsonify({"message": "PATCH: you made a change to one field in a record"}), 200


# @app.route('/whatsmymethod', methods=["DELETE"])
# def delete_method():
#     return jsonify({"message": "No DELETE. use deactivate instead"}), 200

# @app.route('/json')
# def read_products():
#     return jsonify({"message": "this return includes a status code"}), 200


