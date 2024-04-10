from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv


app = Flask(__name__)
db = SQLAlchemy()
load_dotenv()

CONFIG = os.getenv("CONFIG")
SECRET_KEY = os.getenv('KEY')
def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    from .views import views
    from .auth import auth
    from .models import Customer, Cart, Product, Order
    from .product_search import productsearch

    app.register_blueprint(views, url_prefix='/') # localhost:5000/about-us
    app.register_blueprint(auth, url_prefix='/') # localhost:5000/auth/change-password
    app.register_blueprint(productsearch, url_prefix='/')


    with app.app_context():
        create_database()

    return app

def create_database():
    db.create_all()
    print('Database Created')