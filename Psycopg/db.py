# CREATE TABLE IF NOT EXISTS Companies(
#   company_id SERIAL PRIMARY KEY,
#   company_name VARCHAR UNIQUE NOT NULL
# );

# CREATE TABLE IF NOT EXISTS Categories(
#   category_id SERIAL PRIMARY KEY,
#   category_name VARCHAR UNIQUE NOT NULL
# );

# CREATE TABLE IF NOT EXISTS Products(
#   product_id SERIAL PRIMARY KEY,
#   company_id INTEGER,
#   product_name VARCHAR UNIQUE NOT NULL,
#   price INTEGER,
#   description VARCHAR,
#   active BOOLEAN,
#   FOREIGN KEY (company_id) REFERENCES Companies(company_id)
# );

# CREATE TABLE IF NOT EXISTS Warranties(
#   warranty_id SERIAL PRIMARY KEY,
#   product_id INTEGER,
#   warranty_months INTEGER NOT NULL,
#   FOREIGN KEY (product_id) REFERENCES Products(product_id)
# );

# CREATE TABLE IF NOT EXISTS Products_categories(
#   product_id INTEGER,
#   category_id INTEGER,
#   FOREIGN KEY (product_id) REFERENCES Products(product_id),
#   FOREIGN KEY (category_id) REFERENCES Categories(category_id)
# );