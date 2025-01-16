from flask import render_template # type: ignore

def home():
    return render_template('home.html')

def about():
    return render_template('about.html')
