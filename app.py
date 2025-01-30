from flask import Flask  # type: ignore
import views

app = Flask(__name__)

# Define URL rules for each page
app.add_url_rule('/', 'home', views.home)
app.add_url_rule('/about', 'about', views.about)
app.add_url_rule('/contact', 'contact', views.contact)
app.add_url_rule('/booknow', 'book_now', views.book_now)
<<<<<<< HEAD
app.add_url_rule('/signup', 'signup', views.signup)
app.add_url_rule('/login', 'login', views.login)

if __name__ == '__main__':
    app.run()
=======
app.add_url_rule('/signup', 'signup', views.signup, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', views.login, methods=['GET', 'POST'])
app.add_url_rule('/screen', 'screen', views.screen)
app.add_url_rule('/profile', 'profile', views.profile)
if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> master
