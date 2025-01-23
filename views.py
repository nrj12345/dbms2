from flask import render_template  # type: ignore

def home():
    return render_template('home.html')

def about():
    return render_template('about.html')

def contact():
    return render_template('contact.html')

def book_now():
    return render_template('booknow.html')

def signup():
    return render_template('signup.html')

def login():
    return render_template('login.html')
