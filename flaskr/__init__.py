import base64
from datetime import datetime
import io
from mailbox import Message, Mailbox
import mailbox
import re
import secrets
import string
from flask import Flask, app, flash, jsonify, logging, redirect, send_file, session, render_template, request, url_for
from .db import get_db,query_db,execute_db
from flask_bcrypt import Bcrypt
from flask_bcrypt import check_password_hash
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from authlib.integrations.flask_client import OAuth
from flask_cors import CORS
from flask_mail import Mail
from mailbox import Message
from flask_sqlalchemy import SQLAlchemy

def generate_secret_key(length=32):
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*()-=_+'
    return ''.join(secrets.choice(alphabet) for _ in range(length))



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'

    app.config['UPLOAD_FOLDER'] = 'static/uploads'

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Google OAuth configuration
    app.config['GOOGLE_CLIENT_ID'] = "431195197375-5moggpoor3nl6ej4g8rmsvvuedhci4l5.apps.googleusercontent.com"
    app.config['GOOGLE_CLIENT_SECRET'] = "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"
    app.config['GOOGLE_DISCOVERY_URL'] = "https://accounts.google.com/.well-known/openid-configuration"

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = "nw.nilusha@gmail.com"
    app.config["MAIL_PASSWORD"] = "pjnm dfyd ulgx bowk"
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True

    mail = Mail(app)

    oauth = OAuth(app)
    oauth.register(
        name='google',
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        access_token_url='https://oauth2.googleapis.com/token',
        userinfo_endpoint='https://www.googleapis.com/oauth2/v3/userinfo',
        jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
        client_kwargs={'scope': 'openid profile email'},
        # redirect_uri='https://advertisementhub-fa406cdf9ed7.herokuapp.com/authorize',
    )

    bcrypt = Bcrypt(app)

    user_logged = ''

    @app.route('/', methods=['GET', 'POST'])
    def appInit():
       return render_template('login.html')
    
    @app.route("/send_mail", methods=['GET', 'POST'])
    def send_mail():
        try:
            recipient = request.form['recipient-email'] 
            title = request.form['title']
            message_body = request.form['message-body']

            # Create a message object
            mail_message = Message(
                subject=title,
                recipients=[recipient],
                body=message_body,
                sender=app.config['nw.nilusha@gmail.com']  # Correct usage
            )
            
            # Send the email
            mail.send(mail_message)
            
            return jsonify({"message": "Mail has sent", "status":True}), 200
        except KeyError as e:
            return jsonify({"message": "Mail has sent fail", "status":False}), 500
        except Exception as e:
            return jsonify({"message": "Mail has sent fail", "status":False}), 500


    @app.route('/login_app', methods=['GET', 'POST'])
    def login_app():
        print("Inside login module")
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = query_db("SELECT username, password, userRole, userID FROM Users WHERE username = ?",[username],one=True)
            print("After sql command")
            print(f"User---> {user}")

            if user:
                hashed_password = user['password']

                if check_password_hash(hashed_password, password):
                    user_logged = username
                    session['username'] = username
                    session['userRole'] = user['userRole']
                    session['userID'] = user['userID']

                    return jsonify({"user": user['username'], "message": "Success"}), 200
                else:
                    return jsonify({"user": "nil", "message": "Incorrect Username or Password"}), 500
            else:
                return jsonify({"user": "nil", "message": "Incorrect Username or Password"}), 500
        else:
            return render_template('login.html')
    
    
    @app.route('/google_login')
    def google_login():
        redirect_uri = url_for('authorize', _external=True)
        google = oauth.create_client('google')
        return google.authorize_redirect(redirect_uri)


    @app.route('/authorize')
    def authorize():
        token = oauth.google.authorize_access_token()
        user_info = token['userinfo']
        if user_info:
            # Extract the email or preferred username from the user info
            email = user_info.get('email')
            username = email.split('@')[0] if email else 'unknown'
            
            # Store the username and user role in the session
            session['username'] = username
            session['userRole'] = 'User'
            return redirect(url_for('home'))
            # return jsonify({"user": username, "message": "Success"}), 200
        else:
            return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.clear()
        return render_template('login.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        return render_template('signup.html')
    
    @app.route('/home', methods=['GET', 'POST'])
    def home():
        if session['username']:
            try:
                username = session['username']
                userrole = session['userRole']
                userDetails = {
                    'Username': username,
                    'UserRole': userrole,
                }
                return render_template('home.html', userData=userDetails)
            except KeyError as e:
                app.logger.error('Session data KeyError in home route: %s', e)
                return render_template('error.html', error_message='Session data error occurred')
            except Exception as e:
                app.logger.error('Error rendering home page: %s', e)
                return render_template('error.html', error_message='Error rendering home page')
        else:
            app.logger.info('User not logged in, redirecting to login page from home')
            return redirect(url_for('login_app'))
    
    @app.route('/edit_advertisement', methods=['GET', 'POST'])
    def edit_advertisement():
        if request.method == 'POST': 
            if 'username' not in session:
                # Redirect to login if username not found in session
                app.logger.info('User not logged in, redirecting to login page')
                return redirect(url_for('login_app'))

            addId = request.form['adId']
            username = session['username']
            print(f"Test---->{addId}")
            print(f"Username---->{username}")

            app.logger.info('User %s is editing ad with id %s', username, addId)
            
            try:
                data = query_db("SELECT * FROM Advertisement WHERE addID=?", [addId], one=True)
                print(f"Data----->{data}")
                if data:
                    ad_data = {
                        'AdId': data['addID'],
                        'UserName':username,
                        'AdTitle': data['addTitle'],
                        'AdPrice': data['addPrice'],
                        'AdContact': data['addContact'],
                        'AdEmail': data['addEmail'],
                        'AdSpecification': data['addSpecification'],
                        'AdDescription': data['addInformation'],
                        'AdCategory': data['category'],
                        
                    }
                    app.logger.info('Ad data retrieved for ad_id %s', addId)
                    return render_template('new_ad.html', adDataUpdate=ad_data)
                else:
                    app.logger.warning('No ad found with ad_id %s', addId)
                    return render_template('error.html', error_message='No ad found with the provided ID')
            except Exception as e:
                app.logger.error('Error fetching ad data: %s', e)
                return render_template('error.html', error_message='Error retrieving ad data')


    @app.route('/new_advertisement', methods=['GET', 'POST'])
    def new_advertisement():  
        if session['username']:
            username = session['username']
            print(f"New add user -----> {username}")
            ad_data = {
                'AdId': 0,
                'UserName': username,
            }
            app.logger.info('Creating new ad for user %s', username)
            return render_template('new_ad.html', adDataUpdate=ad_data)
        else:
            return render_template('login.html')
    
    @app.route('/about_us', methods=['GET', 'POST'])
    def about_us():
        if session['username']:
            try:
                username = session['username']
                Results = {
                    'Username': username,
                }
                return render_template('about_us.html', userData=Results)
            except Exception as e:
                app.logger.error('Error rendering about us page: %s', e)
                return render_template('error.html', error_message='Error rendering about us page')
        else:
            app.logger.info('User not logged in, redirecting to login page from about_us')
            return redirect(url_for('login_app'))
        
    
    @app.route('/contact_us', methods=['GET', 'POST'])
    def contact_us():
        if session['username']:
            username = session['username']
            userrole = session['userRole']
            userDetails = {
                'Username': username,
                'UserRole': userrole,
            }
            username = session['username']
            return render_template('contact_us.html',userData=userDetails)
        else:
            return redirect(url_for('login_app'))
        
    @app.route('/send_message', methods=['POST'])
    def send_message():
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        msg = Message(subject=f"Contact Form Submission from {name}",
                    sender='nw.nilusha@gmail.com',
                    recipients=['your_email@example.com'], 
                    body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")
        
        try:
            mailbox.send(msg)
            flash('Message sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send message: {e}', 'danger')
        
        return redirect(url_for('contact_us'))
    
    def convert_to_binary(filename):
        with open(filename, 'rb') as file:
            binary_data = file.read()
        return binary_data
    
    def username_exists(username):
        user = query_db('select * from Users where username = ?',[username], one=True)
        if user:
            print('User available')
            return user
        else:
           print('None User')
           return  None
    
    def is_valid_email(email):
        email_regex = r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$"

        if re.match(email_regex, email):
            return True
        else:
            return False
    
    @app.route('/manage_users', methods=['GET', 'POST'])
    def manageUsers():
            username = request.form['create_username']
            password = request.form['create_password']
            email = request.form['create_email']
            confirmPassword = request.form['create_confirm_password']
            role = "User"
    
            if username_exists(username):
                error_msg = 'Username already exists. Please use another Username.'
                return jsonify({"message": error_msg, "status":False}), 500

            if (len(password) < 4):
                error_msg = 'Password must be atleast 4 characters'
                return jsonify({"message": error_msg, "status":False}), 500
            
            if (password != confirmPassword):
                error_msg = 'Passwords are not matching. Please re enter password.'
                return jsonify({"message": error_msg, "status":False}), 500

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            try:
                execute_db('INSERT INTO Users (username, password, email, userRole) VALUES (?,?,?,?)',[username,hashed_password,email,role],)
                msg = username + ' - registered successfully!'
                return jsonify({"message": msg, "status":True}), 200
            except Exception as e:
                # db.rollback()
                error_msg = f'Error inserting user: {e}'
                return jsonify({"message": error_msg, "status":False}), 500
    

    # Get all Ad list
    @app.route('/get_ads/<string:ad_category>')
    def get_ads(ad_category):
        app.logger.info('Fetching ads for category: %s', ad_category)
        
        try:
            ad_data = fetch_all_ads(ad_category)
            
            results = [{
                'AdId': ad['addID'],
                'UserId': ad['userID'],
                'UserName': ad['username'],
                'AdTitle': ad['addTitle'],
                'AdDate': ad['addDate'],
                'AdPrice': ad['addPrice'],
                'AdContact': ad['addContact'],
                'AdEmail': ad['addEmail'],
                'AdSpecification': ad['addSpecification'],
                'AdDescription': ad['addInformation'],
                'AdCategory': ad['category'],
                'logedUserName': session.get('username', '')
            } for ad in ad_data]

            response = {'Results': results, 'count': len(results)}
            return jsonify(response)
        
        except Exception as e:
            app.logger.error('Error fetching ads: %s', e)
            return jsonify({'error': 'An error occurred while fetching ads'}), 500
    
     # Fetch all data from Advertisement tables.
    def fetch_all_ads(ad_cat):
        data = None
        if ad_cat == 'All':
            data = query_db("SELECT  * FROM Advertisement",[],)
        else:
            data = query_db("SELECT  * FROM Advertisement WHERE category=?",[ad_cat],)

        return data
    
    @app.route('/get_ad', methods=['POST'])
    def get_ad():
        ad_id = request.args.get('adId')
        try:
            data = query_db("SELECT  * FROM Advertisement WHERE addID=?",[ad_id],one=True)
            Results = {
                'AdId': data['addID'],
                'UserId' : data['userID'],
                'UserName' : data['username'],
                'AdTitle': data['addTitle'],
                'AdDate' : data['addDate'],
                'AdPrice': data['addPrice'],
                'AdContact': data['addContact'],
                'AdEmail': data['addEmail'],
                'AdSpecification' : data['addSpecification'],
                'AdDescription': data['addInformation'],
                'AdCategory': data['category'],
            }
            print(Results.Image)
            response = {'Results': Results}
            return jsonify(response)
        except Exception as e:
            db.rollback()
            return jsonify({"message": "New Ad unsuccessful"}), 500


    @app.route('/submit_ad', methods=['POST'])
    def submit_ad():
        if request.method == 'POST':
            title = request.form['ad-title']
            price = request.form['ad-price']
            contact = request.form['ad-contact']
            email = request.form['ad-email']
            specification = request.form['ad-specification']
            description = request.form['ad-description']
            category = request.form['ad-category']
            if 'userID' in session:
                userId = session['userID']
            else:
                userId = 0
            userName = session['username']
            adDate = datetime.today().strftime('%Y-%m-%d')

            try:
                execute_db(
                    'INSERT INTO Advertisement (userID, userName, addTitle, addDate, addPrice, addContact, addEmail,addSpecification, addInformation, category) VALUES (?,?,?,?,?,?,?,?,?,?)', 
                    [userId,userName,title,adDate,price,contact,email,specification,description, category],
                )
                return jsonify({"title":"Save Ad Successful","message": "New Ad completed successfully","status":True}), 200
            except Exception as e:
                db.rollback()
                return jsonify({"title":"Save Ad Error","message": "New Ad unsuccessful","status":False}), 500
    

            # if 'ad-image' not in request.files:
            #     return jsonify({"message": "No Image Selected"}), 500
            
            # file = request.files['ad-image']

            # if file.filename == '':
            #     return jsonify({"title":"Save Ad Error","message": "No Image Selected","status":False}), 500
            
            # if file:
            #     image_data = file.read()

            #     db = get_db()
            #     cursor = db.cursor()
            #     try:
            #         cursor.execute('INSERT INTO Advertisement (userID, addTitle, addPrice, addContact, addEmail, addInformation, category, image) VALUES (%s, %s, %s,%s, %s, %s,%s,%s)', (userId, title,price,contact,email, description, category, image_data))
            #         db.commit()
            #         return jsonify({"title":"Save Ad Successful","message": "New Ad completed successfully","status":True}), 200
            #     except Exception as e:
            #         db.rollback()
            #         return jsonify({"title":"Save Ad Error","message": "New Ad unsuccessful","status":False}), 500
            #     finally:
            #         cursor.close()
            # return jsonify({"title":"Save Ad Error","message": "No Image Selected","status":False}), 500
                
        return render_template('new_ad.html')
        

    @app.route('/update_ad/<string:ad_id>', methods=['POST'])
    def update_ad(ad_id):
        try:
            if request.method == 'POST':
                title = request.form['ad-title']
                price = request.form['ad-price']
                contact = request.form['ad-contact']
                email = request.form['ad-email']
                specification = request.form['ad-specification']
                description = request.form['ad-description']
                category = request.form['ad-category']

                try:
                    execute_db('UPDATE Advertisement SET addTitle = ?, addPrice = ?, addContact = ?, addEmail = ?,addSpecification= ?, addInformation = ?, category = ? WHERE addID = ?', 
                                   [title,price,contact,email,specification,description,category,ad_id],
                                   )
                    return jsonify({"title":"Update Ad Unsuccessful","message": "Ad updated successfully","status":True}), 200
                except Exception as e:
                    db.rollback()
                    return jsonify({"title":"Update Ad Unsuccessful","message": "Ad updated unsuccessful","status":False}), 500

            return jsonify({"title":"Update Ad Unsuccessful","message": "Ad updated unsuccessful","status":False}), 500
        except Exception as e:
            logging.error(f"Failed to update Ad details: {str(e)}")
            return jsonify({"title":"Update Ad Unsuccessful","message": "Ad updated unsuccessful","status":False}), 500
    
    # Delete Ad from Device and CompanyManufacturedDevice tables.
    @app.route('/delete_ad/<string:ad_id>', methods=['DELETE'])
    def delete_add(ad_id): 
        print('Inside delete Ad')
        try:
            execute_db("DELETE FROM Advertisement WHERE addID = ?", [ad_id],) 
            return jsonify({"title":"Delete Ad","message": "Delete advertisement successful","status":True}), 200
        except Exception as e:
            return jsonify({"title":"Delete Ad","message": "Delete advertisement Unsuccessful","status":True}), 500
    
    @app.route('/get_ad_image', methods=['POST'])
    def get_ad_image():
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT image FROM Advertisement WHERE addID = %s", (1,))
            data = cursor.fetchone()
            cursor.close()  
            return send_file(io.BytesIO(data), mimetype='image/jpeg')
        except Exception as e:
            return jsonify({"error": "Failed to delete Ad", "details": str(e)}), 500


    return app

app = create_app()
