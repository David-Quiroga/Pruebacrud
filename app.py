from flask import Flask, jsonify, request, render_template
from psycopg2 import connect, extras
from os import environ
#from dotenv import load_dotenv

#load_dotenv()

app = Flask(__name__)

host = 'localhost'
port = 5432
dbname = 'crud'
user = 'postgres'
password = 'Campos0430'


def get_db_connection():
    conn = connect(host=host, dbname=dbname,
                user=user, password=password, port=port)
    return conn


@app.get('/api/users')
def get_users():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)


@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    company  = new_user['company']
    email    = new_user['email']
    descrip  = new_user['descrip']
    sector   = new_user['sector']
    conn     = get_db_connection()
    cur      = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("INSERT INTO users (company, email, descrip, sector) VALUES (%s, %s, %s, %s) RETURNING *",
                (company, email, descrip, sector))
    new_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_user)


@app.get('/api/users/<id>')
def get_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    return jsonify(user)


@app.put('/api/users/<id>')
def update_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    new_user = request.get_json()
    company  = new_user['company']
    descrip  = new_user['descrip']
    email    = new_user['email']
    sector   = new_user['sector']
    cur.execute("UPDATE users SET company = %s, email = %s, descrip = %s, sector = %s WHERE id = %s RETURNING *",
                (company, email, descrip, sector,  id))
    updated_user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if updated_user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(updated_user)


@app.delete('/api/users/<id>')
def delete_user(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("DELETE FROM users WHERE id = %s RETURNING *", (id,))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


@app.get('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)