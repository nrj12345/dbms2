from flask import Flask  # type: ignore
import views

app = Flask(__name__)

# Define URL rules for each page
app.add_url_rule('/', 'home', views.home)
app.add_url_rule('/about', 'about', views.about)
app.add_url_rule('/contact', 'contact', views.contact)
app.add_url_rule('/booknow', 'book_now', views.book_now)
app.add_url_rule('/signup', 'signup', views.signup)
app.add_url_rule('/login', 'login', views.login)

if __name__ == '__main__':
    app.run()
