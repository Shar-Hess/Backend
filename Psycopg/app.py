from flask import Flask, jsonify, request
import psycopg2
import os

from routes.company_routes import company


database_name = os.environ.get("DATABASE_NAME")
app_host = os.environ.get('APP_HOST')
app_port = os.environ.get('APP_PORT')

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

app = Flask(__name__)

# Products routes and controllers

@app.route('/product', methods=['POST'])
def create_product():
    post_data = request.form if request.form else request.get_json()

    product_name = post_data.get('product_name')
    description = post_data.get('description')
    price = post_data.get('price')

    if not product_name:
        return jsonify({"message": "product_name is a required field"}), 400

    result = cursor.execute("""
        SELECT * FROM products
            WHERE product_name=%s
        """,
        (product_name,)
    )

    result = cursor.fetchone()

    if result:
        return jsonify({"message": 'Product already exists'}), 400

    cursor.execute("""
        INSERT INTO products
            (product_name, description, price)
            VALUES(%s, %s, %s)
        """,
        (product_name, description, price)
    )

    conn.commit()
    return jsonify({"message": f"Product {product_name} added to DB"}), 201


@app.route('/products', methods=["GET"])
def read_products():
    result = cursor.execute("""
        SELECT * FROM Products;
    """)

    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'product_id': record[0],
            'product_name': record[1],
            'description': record[2],
            'price': record[3],
            'active': record[4]
        }

        record_list.append(record)

    return jsonify({"message": "products found", "results": record_list}), 200

@app.route('/product/<product_id>', methods=["GET"])
def get_product_by_id(product_id):
    result = cursor.execute("""
        SELECT * FROM Products
        WHERE product_id=%s;
    """, (product_id,))
    
    result = cursor.fetchone()

    if result:
        return jsonify({"message": "product found", "results": result})
    else:
        return jsonify({"message": "product not found"}), 404

@app.route('/products', methods=["GET"])
def get_active_products():
    active = request.args.get('active', default='false', type=str).lower() in ['true', '1', 't', 'y', 'yes']

    cursor.execute("""
        SELECT * FROM Products
        WHERE active=%s;
    """, (active,))

    results = cursor.fetchall()

    if results:
        products_list = []
        for product in results:
            product_record = {
                'product_id': product[0],
                'product_name': product[1],
                'description': product[2],
                'price': product[3],
                'active': product[4]
            }
            products_list.append(product_record)

        return jsonify({"message": "products found", "results": products_list})
    else:
        return jsonify({"message": "no products found"}), 404


@app.route('/products/<product_id>', methods=["PUT"])
def update_product_by_id(product_id):

    post_data = request.form if request.form else request.get_json()
    update_fields = {}

    if 'product_name' in post_data:
        update_fields['product_name'] = post_data['product_name']
    if 'description' in post_data:
        update_fields['description'] = post_data['description']
    if 'price' in post_data:
        try:
            update_fields['price'] = float(post_data['price']) 
        except ValueError:
            return jsonify({"error": "'price' must be a valid number"}), 400
    if 'active' in post_data:
        update_fields['active'] = bool(post_data['active'])
    
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400


    set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
    values = list(update_fields.values())
    values.append(product_id) 

    query = f"""
        UPDATE Products
        SET {set_clause}
        WHERE product_id = %s;
    """

    try:

        cursor.execute(query, tuple(values))
        cursor.execute("""
            SELECT * FROM Products
            WHERE product_id = %s;
        """, (product_id,))

        result = cursor.fetchone()

        if result is None:
            return jsonify({"message": "Product not found"}), 404


        conn.commit()

        return jsonify({"message": "Updated", "results": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/product/delete/<product_id>', methods=['DELETE'])
def delete_product_by_id(product_id):
    product = {}
    product['product_id'] = int(product_id)

    if not product['product_id']:
        return jsonify({"message": "Product ID is required"}), 400
    
    try:
        cursor.execute("""
            SELECT * FROM Products
            WHERE product_id = %s;
            """, (product_id, ))
        
        result = cursor.fetchone()

        if result:
            cursor.execute("""
                DELETE FROM Products
                WHERE product_id = %s;
                """, (product_id, ))
            
            conn.commit()
            return jsonify({"message": "Product Deleted"}), 200
    
        else: 
            return jsonify({"message": "No product found"}), 404
        
    except Exception as e:
        print(e)
        return jsonify({"message": "Product could not be deleted"})

# Company routes and controllers     

@app.route('/company', methods=['POST'])
def create_company():
    post_data = request.form if request.form else request.get_json()

    company_name = post_data.get('company_name')

    if not company_name:
        return jsonify({"message": "company_name is a required field"}), 400

    result = cursor.execute("""
        SELECT * FROM companies
            WHERE company_name=%s
        """,
        (company_name,)
    )

    result = cursor.fetchone()

    if result:
        return jsonify({"message": 'Company already exists'}), 400

    cursor.execute("""
        INSERT INTO companies
            (company_name)
            VALUES(%s)
        """,
        (company_name, )
    )

    conn.commit()
    return jsonify({"message": f"company {company_name} added to DB"}), 201


@app.route('/companies', methods=["GET"])
def read_companies():
    result = cursor.execute("""
        SELECT * FROM companies;
    """)

    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'company_id': record[0],
            'company_name': record[1]
        }

        record_list.append(record)

    return jsonify({"message": "companies found", "results": record_list}), 200

@app.route('/company/<company_id>', methods=["GET"])
def read_company_by_id(company_id):
    result = cursor.execute("""
        SELECT * FROM companies
            WHERE company_id=%s;
    """, 
    (company_id,)
    )

    result = cursor.fetchone()

    if result:
        return jsonify({"message": "company found", "results": result})
    else:
        return jsonify({"message": "product not found"}), 404


@app.route('/company/<company_id>', methods=["PUT"])
def update_company_by_id(company_id):

    post_data = request.form if request.form else request.get_json()
    
    update_fields = {}

    if 'company_name' in [post_data]:
        update_fields['company_name'] = [post_data]['company_name']

    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
    values = list(update_fields.values())
    values.append(company_id)  


    query = f"""
        UPDATE companies
        SET {set_clause}
        WHERE company_id = %s;
    """

    try:
        cursor.execute(query, tuple(values))

        cursor.execute("""
            SELECT * FROM companies
            WHERE company_id = %s;
        """, (company_id,))

        result = cursor.fetchone()

        if result is None:
            return jsonify({"message": "Company not found"}), 404

        conn.commit()

        return jsonify({"message": "Updated", "results": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/company/delete/<company_id>', methods=['DELETE'])
def delete_company_by_id(company_id):
    company = {}
    company['company_id'] = int(company_id)

    if not company['company_id']:
        return jsonify({"message": "Company ID is required"}), 400
    
    try:
        cursor.execute("""
            SELECT * FROM companies
            WHERE company_id = %s;
            """, (company_id, ))
        
        result = cursor.fetchone()

        if result:
            cursor.execute("""
                DELETE FROM companies
                WHERE company_id = %s;
                """, (company_id, ))
            
            conn.commit()
            return jsonify({"message": "Company Deleted"}), 200
    
        else: 
            return jsonify({"message": "No company found"}), 404
        
    except Exception as e:
        print(e)
        return jsonify({"message": "Company could not be deleted"})


# Category routes and controllers     

@app.route('/category', methods=['POST'])
def create_category():
    post_data = request.form if request.form else request.get_json()

    category_name = post_data.get('category_name')

    if not category_name:
        return jsonify({"message": "category_name is a required field"}), 400

    result = cursor.execute("""
        SELECT * FROM categories
            WHERE category_name=%s
        """,
        (category_name,)
    )

    result = cursor.fetchone()

    if result:
        return jsonify({"message": 'category already exists'}), 400

    cursor.execute("""
        INSERT INTO categories
            (category_name)
            VALUES(%s)
        """,
        (category_name, )
    )

    conn.commit()
    return jsonify({"message": f"category {category_name} added to DB"}), 201


@app.route('/categories', methods=["GET"])
def read_categories():
    result = cursor.execute("""
        SELECT * FROM categories;
    """)

    result = cursor.fetchall()

    record_list = []

    for record in result:
        record = {
            'category_id': record[0],
            'category_name': record[1]
        }

        record_list.append(record)

    return jsonify({"message": "categories found", "results": record_list}), 200

@app.route('/category/<category_id>', methods=["GET"])
def read_category_by_id(category_id):
    cursor.execute("""
        SELECT * FROM categories
        WHERE category_id=%s;
    """, (category_id,))

    result = cursor.fetchone()

    if result:
        return jsonify({"message": "category found", "results": result})
    else:
        return jsonify({"message": "category not found"}), 404

@app.route('/category/<category_id>', methods=["PUT"])
def update_category_by_id(category_id):
    post_data = request.form if request.form else request.get_json()
    update_fields = {}

    if 'category_name' in post_data:
        update_fields['category_name'] = post_data['category_name']

    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400

    set_clause = ", ".join([f"{key} = %s" for key in update_fields.keys()])
    values = list(update_fields.values())
    values.append(category_id)  


    query = f"""
        UPDATE categories
        SET {set_clause}
        WHERE category_id = %s;
    """

    try:
        cursor.execute(query, tuple(values))

        cursor.execute("""
            SELECT * FROM categories
            WHERE category_id = %s;
        """, (category_id,))

        result = cursor.fetchone()

        if result is None:
            return jsonify({"message": "Category not found"}), 404

        conn.commit()

        return jsonify({"message": "Updated", "results": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/category/delete/<category_id>', methods=['DELETE'])
def delete_category_by_id(category_id):
    category = {}
    category['category_id'] = int(category_id)

    if not category['category_id']:
        return jsonify({"message": "category ID is required"}), 400
    
    try:
        cursor.execute("""
            SELECT * FROM categories
            WHERE category_id = %s;
            """, (category_id, ))
        
        result = cursor.fetchone()

        if result:
            cursor.execute("""
                DELETE FROM categories
                WHERE category_id = %s;
                """, (category_id, ))
            
            conn.commit()
            return jsonify({"message": "category Deleted"}), 200
    
        else: 
            return jsonify({"message": "No category found"}), 404
        
    except Exception as e:
        print(e)
        return jsonify({"message": "category could not be deleted"})


# Warranty #routes and controllers     

@app.route('/warranty', methods=['POST'])
def create_warranty():
    post_data = request.form if request.form else request.get_json()

    product_id = post_data.get('product_id')

    warranty_months = post_data.get('warranty_months')

    if not product_id:
        return jsonify({"message": "product_id is a required field"}), 400

    result = cursor.execute("""
        SELECT * FROM warranties
            WHERE product_id=%s
        """,
        (product_id,)
    )

    result = cursor.fetchone()

    if result:
        return jsonify({"message": 'warranty already exists'}), 400

    cursor.execute("""
        INSERT INTO warranties
            (product_id, warranty_months)
            VALUES(%s, %s)
        """,
        (product_id, warranty_months, )
    )

    conn.commit()
    return jsonify({"message": f"warranty added to product id - {product_id} added to DB"}), 201


@app.route('/warranty/<warranty_id>', methods=["GET"])
def read_warranty_by_id(warranty_id):
    cursor.execute("""
        SELECT * FROM warranties
        WHERE warranty_id=%s;
    """, (warranty_id,))

    result = cursor.fetchone()

    if result:
        return jsonify({"message": "warranty found", "results": result})
    else:
        return jsonify({"message": "warranty not found"}), 404


@app.route('/warranty/<warranty_id>', methods=["PUT"])
def update_warranty_by_id(warranty_id):
    post_data = request.form if request.form else request.get_json()

    if 'warranty_months' not in post_data:
        return jsonify({"error": "'warranty_months' is required"}), 400
    
    warranty_months = post_data['warranty_months']
    
    query = """
        UPDATE warranties
        SET warranty_months = %s
        WHERE warranty_id = %s;
    """

    try:
        cursor.execute(query, (warranty_months, warranty_id))

        cursor.execute("""
            SELECT * FROM warranties
            WHERE warranty_id = %s;
        """, (warranty_id,))

        result = cursor.fetchone()
        if result is None:
            return jsonify({"message": "Warranty not found"}), 404

        conn.commit()

        return jsonify({"message": "Updated", "results": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/warranty/delete/<warranty_id>', methods=['DELETE'])
def delete_warranty_by_id(warranty_id):
    warranty = {}
    warranty['warranty_id'] = int(warranty_id)

    if not warranty['warranty_id']:
        return jsonify({"message": "warranty ID is required"}), 400
    
    try:
        cursor.execute("""
            SELECT * FROM warranties
            WHERE warranty_id = %s;
            """, (warranty_id, ))
        
        result = cursor.fetchone()

        if result:
            cursor.execute("""
                DELETE FROM warranties
                WHERE warranty_id = %s;
                """, (warranty_id, ))
            
            associated_product = cursor.fetchone()
            
            if associated_product:
                cursor.execute("""
                    DELETE FROM products
                    WHERE product_id = %s;
                    """, (associated_product['product_id'],))
            
            conn.commit()
            return jsonify({"message": "warranty Deleted"}), 200
    
        else: 
            return jsonify({"message": "No warranty found"}), 404
        
    except Exception as e:
        print(e)
        return jsonify({"message": "warranty could not be deleted"})

if __name__ == '__main__':
    app.run(host=app_host, port=app_port)


