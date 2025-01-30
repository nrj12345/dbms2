from flask import render_template, request, redirect, url_for, make_response
from models import User, SessionLocal

def home():
    return render_template('home.html')

def about():
    return render_template('about.html')

def contact():
    return render_template('contact.html')

def book_now():
    return render_template('booknow.html')

def screen():
    return render_template('screen.html')

def profile():
    return render_template('profile.html')

def signup():
    if request.method == 'GET':
        return render_template('signup.html')  # Render signup form on GET request

    # Handle form submission on POST request
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    if password != confirm_password:
        error = 'Passwords do not match'
        return render_template('signup.html', error=error)

    # Create user object and set password
    user = User(email=email, name=name)
    user.set_password(password)

    # Connect to database and add user
    db = SessionLocal()
    db.add(user)
    db.commit()
    db.close()

    # Create a response object to set the cookie with a 5-minute lifespan
    response = make_response(redirect(url_for('home')))
    response.set_cookie('user_email', email, max_age=10 * 60)  # Cookie valid for 5 minutes (300 seconds)

    return response


def login():
    if request.method == 'GET':
        return render_template('login.html')  # Render login form

    email = request.form['email']
    password = request.form['password']

    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()
    db.close()

    if not user or not user.check_password(password):
        error = 'Invalid email or password'
        return render_template('login.html', error=error)

    # Set a cookie for 5 minutes if login is successful
    response = make_response(redirect(url_for('home')))
    response.set_cookie('user_email', email, max_age=600)  # 300 seconds = 5 minutes
    return response

