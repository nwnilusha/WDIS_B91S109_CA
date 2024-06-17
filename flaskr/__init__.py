import secrets
import string
from flask import Flask, redirect, render_template, request, url_for
from .db import get_db

def generate_secret_key(length=32):
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*()-=_+'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = generate_secret_key()

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'dbs'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DB'] = 'WDIS'

    @app.route('/', methods=['GET', 'POST'])
    def login():
       print("Inside login module")
       if request.method == 'POST':
            username = request.form['email']
            password = request.form['password']

            db = get_db()
            cursor = db.cursor()
            cursor.execute('SELECT username, password FROM Users WHERE username = %s AND password = %s;', (username,password))
            user = cursor.fetchone()
            cursor.close()

            if user:
                return render_template('home.html')
            else:
                msg = 'Incorrect Username or Password'
                return render_template('login.html', msg=msg)
       else:
        msg = 'Incorrect Username or Password'
        return render_template('signup.html', msg=msg)
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return render_template('signup.html')
    
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        return render_template('home.html')
    

    return app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080') # indent this line