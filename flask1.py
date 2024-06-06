from flask import Flask, request, redirect, url_for, render_template
import mysql.connector
import yaml

app = Flask(__name__)

# Database connection


def get_db_connection():
    with open('db_config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    connection = mysql.connector.connect(
        host=config['db']['host'],
        user=config['db']['user'],
        password=config['db']['password'],
        database=config['db']['database']
    )
    return connection


# Home route to display users
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', users=users)


# Create new user
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (%s, %s)', (name, email))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')


# Update user
@app.route('/update/<int:user_id>', methods=('GET', 'POST'))
def update(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        cursor.execute('UPDATE users SET name = %s, email = %s WHERE id = %s', (name, email, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    cursor.close()
    conn.close()
    return render_template('update.html', user=user)


# Delete user
@app.route('/delete/<int:user_id>')
def delete(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = %s', (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
