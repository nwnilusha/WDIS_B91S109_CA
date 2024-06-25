import io
import secrets
import string
from flask import Flask, jsonify, redirect, send_file, session, render_template, request, url_for
from .db import get_db
from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

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
    app.config['UPLOAD_FOLDER'] = 'static/uploads'

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    bcrypt = Bcrypt(app)

    @app.route('/', methods=['GET', 'POST'])
    def login():
       print("Inside login module")
       if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            db = get_db()
            cursor = db.cursor()
            cursor.execute('SELECT username, password, userRole, userID FROM Users WHERE username = %s ', (username,))
            # SELECT username,password, userRole FROM Users WHERE username='admin';
            user = cursor.fetchone()
            cursor.close()
            print("After sql command")

            if user:
                hashed_password = user[1]

                if check_password_hash(hashed_password, password):
                    session['username'] = user[0]
                    session['userRole'] = user[2]
                    session['userID'] = user[3]

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
           return render_template('home.html')

        
    
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return render_template('signup.html')
    
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        return render_template('home.html')
    
    @app.route('/new_advertisement', methods=['GET', 'POST'])
    def new_advertisement():
        return render_template('new_ad.html')
    
    @app.route('/about_us', methods=['GET', 'POST'])
    def about_us():
        return render_template('about_us.html')
    
    @app.route('/contact_us', methods=['GET', 'POST'])
    def contact_us():
        return render_template('contact_us.html')
    
    def convert_to_binary(filename):
        with open(filename, 'rb') as file:
            binary_data = file.read()
        return binary_data
    
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
            confirmPassword = request.form['create_confirm_password']

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
    

    # Get all Ad list
    @app.route('/get_ads')
    def get_ads():
        print('Inside get ads')
        ad_data = fetch_all_ads()
        Results = []
        for row in ad_data:
            Result = {
                'UserId' : row[1],
                'AdTitle': row[2],
                'AdDescription': row[3],
                'AdCategory': row[4],
            }
            Results.append(Result)
        response = {'Results': Results, 'count': len(Results)}
        return jsonify(response)  # Use jsonify to convert response to JSON
    
     # Fetch all data from Advertisement tables.
    def fetch_all_ads():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT  * FROM Advertisement")
        data = cursor.fetchall()
        cursor.close()

        return data
    
    @app.route('/submit_ad', methods=['POST'])
    def submit_ad():
        if request.method == 'POST':
            title = request.form['ad-title']
            description = request.form['ad-description']
            category = request.form['ad-category']
            # userId = session['userID']
            userId = 1

            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute('INSERT INTO Advertisement (userID, addTitle, addInformation, category) VALUES (%s, %s, %s,%s)', (userId, title, description, category))
                db.commit()
                return jsonify({"message": "New Ad completed successfully"}), 200
            except Exception as e:
                db.rollback()
                return jsonify({"message": "New Ad unsuccessful"}), 500
            finally:
                cursor.close()
    
           
            
            # # Check if the post request has the file part
            # if 'ad-image' not in request.files:
            #     return 'No file part'
            
            # file = request.files['ad-image']
            
            # # If the user does not select a file, the browser submits an empty file without a filename
            # if file.filename == '':
            #     return 'No selected file'
            
            # if file:
            #     image_data = file.read()
                
            #     # Save ad information in the database
            #     db = get_db()
            #     cursor = db.cursor()
            #     try:
            #         cursor.execute('INSERT INTO Advertisement (userID, addTitle, addInformation, category, image) VALUES (%s, %s, %s,%s, %s)', (userId, title, description, category, image_data))
            #         db.commit()
            #         msg = 'User registered successfully!'
            #         return render_template('new_ad.html', msg=msg)
            #     except Exception as e:
            #         db.rollback()
            #         error_msg = f'Error inserting user: {e}'
            #         return render_template('new_ad.html', error_msg=error_msg)
            #     finally:
            #         cursor.close()
                
            # return render_template('new_ad.html', msg='No image selected')
        
        return 'Error in form submission'

    
    # @app.route('/ad/<int:ad_id>/image')
    # def get_ad_image(ad_id):
    #     print('Inside get image')
    #     db = get_db()
    #     cursor = db.cursor()
    #     cursor.execute("SELECT image FROM advertisements WHERE id = %s", (ad_id,))
    #     ad = cursor.fetchone()
    #     cursor.close()
    #     if ad:
    #         image = ad[0]
    #         return send_file(io.BytesIO(image), attachment_filename='image.png', mimetype='image/png')
    #     return 'Ad image not found', 404
 

    return app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080') # indent this line