import psycopg2
import os
import flask


database_name = os.environ.get("DATABASE_NAME")

conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()

def create_all():
    print("Creating tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR NOT NULL UNIQUE,
        description VARCHAR,
        price FLOAT,
        active BOOLEAN DEFAULT true
        );
    """)

    conn.commit()
create_all()


def create_product(product_name, description, price):
    cursor.execute("""
        INSERT INTO Products 
            (product_name, description, price)
            VALUES(%s, %s, %s)
        """,
        (product_name, description, price)
    )

    conn.commit()
    return print({"message": f'{product_name} has been added to the Products table.'})

# create_product('Monopoly', 'The game of negotiation', 14.95)
# create_product('Clue', 'The game of deception', 9.95)


def get_product_by_id(product_id):
    result = cursor.execute("""
        SELECT * FROM Products
            WHERE product_id=%s;
    """, 
    (product_id,)
    )

    result = cursor.fetchone()
    return print ({"message": "product found", "results": result})

# get_product_by_id(2)

def get_active_products(active):
    results = cursor.execute("""
        SELECT * FROM Products
            WHERE active=%s;
    """,
    (bool(active),)
    )

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

        return print({"message": "products found", "results": products_list})
    else:
        print("No product found")

get_active_products(False)

def update_products_by_id(product_id, active):
    cursor.execute("""
        UPDATE Products
            SET active = %s
            WHERE product_id = %s;
    """,
    (bool(active), product_id)
    )

    result= cursor.execute("""
        SELECT * FROM Products
            WHERE product_id = %s;
    """,
        (product_id, )
    )

    result = cursor.fetchone()

    conn.commit()
    return print({"message": "Updated", "results": result})

# update_products_by_id(1, False)

