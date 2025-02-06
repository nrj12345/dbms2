from flask import Flask  # type: ignore
import views

app = Flask(__name__)

# Registering a custom Jinja filter to enable zip in templates
@app.template_filter('zip')
def zip_filter(a, b):
    return zip(a, b)

# Define URL rules for each page
app.add_url_rule('/', 'home', views.home)
app.add_url_rule('/about', 'about', views.about)
app.add_url_rule('/contact', 'contact', views.contact)
app.add_url_rule('/booknow', 'book_now', views.book_now)
app.add_url_rule('/signup', 'signup', views.signup, methods=['GET', 'POST'])
app.add_url_rule('/login', 'login', views.login, methods=['GET', 'POST'])
app.add_url_rule('/screen', 'screen', views.screen, methods=['GET'])
app.add_url_rule('/book', 'book', views.book_seats, methods=['POST'])
app.add_url_rule('/profile', 'profile', views.profile)
app.add_url_rule('/admin', 'admin', views.admin, methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug=True)
