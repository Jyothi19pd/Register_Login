from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'secretkey'

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)

# ---------------- LOGIN ----------------
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s AND password=%s', (email, password))
        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            return render_template('user.html', message="Login successful")
        else:
            message = 'Invalid email or password'

    return render_template('login.html', message=message)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email=%s', (email,))
        account = cursor.fetchone()

        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email'
        elif not name or not password:
            message = 'Please fill all fields'
        else:
            cursor.execute('INSERT INTO user (name,email,password) VALUES (%s,%s,%s)',
                           (name, email, password))
            mysql.connection.commit()
            message = 'Registration successful'

    return render_template('register.html', message=message)

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)