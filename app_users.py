from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE_NAME = "simple_users.db"

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_name TEXT NOT NULL,
                   user_age INT NOT NULL)
                   """)
    conn.commit()
    conn.close()


@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return jsonify(users)

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.get_json()
    user_name, user_age = new_user['user_name'], new_user['user_age']
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (user_name, user_age) VALUES (?, ?)", (user_name, user_age))
    conn.commit()
    conn.close()
    return jsonify(new_user)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)