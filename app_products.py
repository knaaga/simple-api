from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

database_name = "simple_store.db"

# initialize the database
def init_db():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_name TEXT NOT NULL,
                    product_cost REAL NOT NULL)
                   """)
    conn.commit()
    conn.close()

# define the routes
@app.route('/products', methods=['GET'])
def get_users():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return jsonify(products)

@app.route('/products', methods=['POST'])
def add_product():
    new_product = request.get_json()
    product_name, product_cost = new_product['product_name'], new_product['product_cost']
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (product_name, product_cost) VALUES (?, ?)", (product_name, product_cost))
    conn.commit()
    conn.close()
    return jsonify(new_product)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
