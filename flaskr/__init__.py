import io
import re
import secrets
import string
from flask import Flask, jsonify, logging, redirect, send_file, session, render_template, request, url_for
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

    app.config['UPLOAD_FOLDER'] = 'static/uploads'

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    bcrypt = Bcrypt(app)

    @app.route('/', methods=['GET', 'POST'])
    def appInit():
       return render_template('login.html')

    @app.route('/login_app', methods=['GET', 'POST'])
    def login_app():
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
                         return jsonify({"user": user[0], "message": "Success"}), 200
                    else:
                         return jsonify({"user": user[0], "message": "Success"}), 200
                else:
                    return jsonify({"user": "nil", "message": "Incorrect Username or Password"}), 500
            else:
                return jsonify({"user": "nil", "message": "Incorrect Username or Password"}), 500
       else:
        #    return render_template('test.html')
        return jsonify({"user": "nil", "message": "Login unsuccessful"}), 500
    
    @app.route('/logout')
    def logout():
        session.clear()
        return render_template('login.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return render_template('signup.html')
    
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        if 'username' in session:
            username = session['username']
            userDetails = {
                    'Username': username,
                }
            return render_template('home.html', userData=userDetails)
        else:
            return render_template('login.html')
    
    @app.route('/new_advertisement', methods=['GET', 'POST'])
    def new_advertisement():
        if 'username' in session:
            username = session['username']
        
            ad_id = request.args.get('adId')

            if ad_id != None:
                print(ad_id)
                db = get_db()
                cursor = db.cursor()
                cursor.execute("SELECT  * FROM Advertisement WHERE addID=%s",(ad_id,))
                data = cursor.fetchall()
                result = data[0]
                Results = {
                        'AdId': result[0],
                        'UserId' : result[1],
                        'AdTitle': result[2],
                        'AdPrice': result[3],
                        'AdContact': result[4],
                        'AdEmail': result[5],
                        'AdDescription': result[6],
                        'AdCategory': result[7],
                        'Username': username,
                    }
                cursor.close()
                
                return render_template('new_ad.html', adDataUpdate=Results)
            else:
                Results = {
                        'AdId': 0,
                    }
                return render_template('new_ad.html', adDataUpdate=Results)
        else:
            # Redirect to login if username not found in session
            return redirect(url_for('login'))

        
    
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
    
    def is_valid_email(email):
        email_regex = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"

        if re.match(email_regex, email):
            return True
        else:
            return False
    
    @app.route('/manage_users', methods=['GET', 'POST'])
    def manageUsers():
        if request.method == 'POST':
            username = request.form['create_username']
            password = request.form['create_password']
            email = request.form['create_email']
            confirmPassword = request.form['create_confirm_password']
            role = "User"

            print(username)
            print(password)
            print(email)
            print(confirmPassword)
    
            if username_exists(username):
                error_msg = 'Username already exists. Please use another Username.'
                return jsonify({"message": error_msg, "status":False}), 500
            
            # if is_valid_email(email):
            #     error_msg = 'Email is not correct format. Please enter correct email.'
            #     return jsonify({"message": error_msg}), 500

            if (len(password) < 4):
                error_msg = 'Password must be atleast 4 characters'
                return jsonify({"message": error_msg, "status":False}), 500
            
            if (password != confirmPassword):
                error_msg = 'Passwords are not matching. Please re enter password.'
                return jsonify({"message": error_msg, "status":False}), 500

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute('INSERT INTO Users (username, password, email, userRole) VALUES (%s, %s, %s, %s)', (username, hashed_password, email, role))
                db.commit()
                msg = username + ' - registered successfully!'
                # return render_template('signin.html', msg=msg)
                return jsonify({"message": msg, "status":True}), 200
            except Exception as e:
                db.rollback()
                error_msg = f'Error inserting user: {e}'
                return jsonify({"message": error_msg, "status":False}), 500
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
                'AdId': row[0],
                'UserId' : row[1],
                'AdTitle': row[2],
                'AdPrice': row[3],
                'AdContact': row[4],
                'AdEmail': row[5],
                'AdDescription': row[6],
                'AdCategory': row[7],
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
    
    @app.route('/get_ad', methods=['POST'])
    def get_ad():
        ad_id = request.args.get('adId')
        print('Inside get ad API')
        print(ad_id)
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT  * FROM Advertisement WHERE addID=%s",(ad_id))
            data = cursor.fetchall()
            Results = {
                'AdId': data[0],
                'UserId' : data[1],
                'AdTitle': data[2],
                'AdPrice': data[3],
                'AdContact': data[4],
                'AdEmail': data[5],
                'AdDescription': data[6],
                'AdCategory': data[7],
            }

            response = {'Results': Results}
            return jsonify(response)
        except Exception as e:
            db.rollback()
            return jsonify({"message": "New Ad unsuccessful"}), 500
        finally:
            cursor.close()


    @app.route('/submit_ad', methods=['POST'])
    def submit_ad():
        if request.method == 'POST':
            title = request.form['ad-title']
            price = request.form['ad-price']
            contact = request.form['ad-contact']
            email = request.form['ad-email']
            description = request.form['ad-description']
            category = request.form['ad-category']
            # userId = session['userID']
            userId = 1

            db = get_db()
            cursor = db.cursor()
            try:
                cursor.execute('INSERT INTO Advertisement (userID, addTitle, addPrice, addContact, addEmail, addInformation, category) VALUES (%s, %s, %s,%s, %s, %s,%s)', (userId, title,price,contact,email, description, category))
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

    # Update device data in Device and CompanyManufacturedDevice tables.
    @app.route('/update_ad/<string:ad_id>', methods=['POST'])
    def update_ad(ad_id):
        try:
            if request.method == 'POST':
                title = request.form['ad-title']
                price = request.form['ad-price']
                contact = request.form['ad-contact']
                email = request.form['ad-email']
                description = request.form['ad-description']
                category = request.form['ad-category']
                # userId = session['userID']
                userId = 1
                print(title);
                print(price);
                print(contact);
                print(email);
                print(description);

                db = get_db()
                cursor = db.cursor()
                try:
                    cursor.execute('UPDATE Advertisement SET addTitle = %s, addPrice = %s, addContact = %s, addEmail = %s, addInformation = %s, category = %s WHERE addID = %s', (title,price,contact,email, description,category, ad_id))
                    db.commit()
                    return jsonify({"message": "Update Ad details successfully"}), 200
                except Exception as e:
                    db.rollback()
                    return jsonify({"message": "Update Ad details unsuccessful"}), 500
                finally:
                    cursor.close()

            return jsonify({"message": "Update Ad details unsuccessful"}), 200
        except Exception as e:
            logging.error(f"Failed to update Ad details: {str(e)}")
            return jsonify({"error": "Failed to update Ad details", "details": str(e)}), 500
    
    # Delete Ad from Device and CompanyManufacturedDevice tables.
    @app.route('/delete_ad/<string:ad_id>', methods=['DELETE'])
    def delete_add(ad_id): 
        print('Inside delete Ad')
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM Advertisement WHERE addID = %s", (ad_id,))
            cursor.close()  # Close the cursor after use
            return jsonify({"message": "Ad deleted successfully"}), 200
        except Exception as e:
            return jsonify({"error": "Failed to delete Ad", "details": str(e)}), 500

    return app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080') # indent this line