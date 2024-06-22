import secrets
import string
from flask import Flask, redirect, session, render_template, request, url_for
from .db import get_db
from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash

def generate_secret_key(length=32):
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*()-=_+'
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = generate_secret_key()

    # app.config['MYSQL_HOST'] = 'localhost'
    # app.config['MYSQL_USER'] = 'dbs'
    # app.config['MYSQL_PASSWORD'] = 'password'
    # app.config['MYSQL_DB'] = 'WDIS'

    bcrypt = Bcrypt(app)

    @app.route('/', methods=['GET', 'POST'])
    def login():
       print("Inside login module")
       if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            print(username)
            print(password)
            db = get_db()
            cursor = db.cursor()
            cursor.execute('SELECT username, password, userRole FROM Users WHERE username = %s ', (username,))
            # SELECT username,password, userRole FROM Users WHERE username='admin';
            user = cursor.fetchone()
            cursor.close()
            print("After sql command")

            if user:
                hashed_password = user[1]
                if check_password_hash(hashed_password, password):
                    session['username'] = user[0]
                    session['userRole'] = user[2]

                    if session['userRole'] == 'admin':
                        return redirect(url_for('home'))
                    else:
                        return redirect(url_for('home'))
                else:
                    msg = 'Incorrect Username or Password'
                    return render_template('login.html', msg=msg)
            else:
                msg = 'Incorrect Username or Password'
                return render_template('login.html', msg=msg)
       else:
        return render_template('login.html')
        # return redirect(url_for('login'))
    
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return render_template('signup.html')
    
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        return render_template('home.html')
    
    def username_exists(username):
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM Users WHERE username=%s', (username,))
        record = cursor.fetchone()
        cursor.close()
        return record is not None
    
    @app.route('/users', methods=['GET', 'POST'])
    def manageUsers():
        if request.method == 'POST':
            username = request.form['create_username']
            password = request.form['create_password']
            email = request.form['create_email']
            confirmPassword = request.form['create_confirm-password']
            # role = request.form['user_role']
            role = "User"
            

            if password != confirmPassword:
                error_msg = 'Passwords are not matching. Please re enter password.'
                return render_template('signup.html', error_msg=error_msg)

            if username_exists(username):
                error_msg = 'Username already exists. Please use another Username.'
                return render_template('signup.html', error_msg=error_msg)

            if len(password) < 4:
                error_msg = 'Password must be atleast 4 characters'
                return render_template('signup.html', error_msg=error_msg)

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            print(username)
            print(password)
            print(confirmPassword)

            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute('INSERT INTO Users (username, password, email, userRole) VALUES (%s, %s, %s, %s)', (username, hashed_password, email, role))
                db.commit()
                msg = 'User registered successfully!'
                return render_template('signup.html', msg=msg)
            except Exception as e:
                db.rollback()
                error_msg = f'Error inserting user: {e}'
                return render_template('signup.html', error_msg=error_msg, username=username, password=password)
            finally:
                cursor.close()
        else:
            return render_template('signup.html')
        
        
    return app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080') # indent this line