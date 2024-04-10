import pytest
from flask import json
from app import create_app
from app.models import Product, Cart
from app.models import db

@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def setup_database(app, mocker):
    """
    Sets up a mocked database environment for each test.
    """
    with app.app_context():
        mocker.patch('app.db.session.add')
        mocker.patch('app.db.session.commit')
def test_add_new_item_to_cart_with_quantity_1(mocker, client, app):
    with app.app_context():
        product_mock = Product(id=1, product_name='Test Product', current_price=10.0, in_stock=10)
        mocker.patch('app.models.Product.query.get', return_value=product_mock)
        mocker.patch('app.models.Cart.query.filter_by', return_value=None)
        data = {'product_id': 1, 'quantity': 1}
        response = client.post('/add-to-cart', data=json.dumps(data), content_type='application/json')
        assert response.status_code == 200
        assert response.json['message'] == 'Test Product added to cart'

def test_returns_json_object(client):
    response = client.get('/cart')
    assert response.status_code == 200
    assert response.is_json
    assert 'cart' in response.json and 'total' in response.json

def test_valid_cart_id_provided(client, app):
    with app.app_context():
        # Setup necessary database records, if not already done
        product = Product(id=1, current_price=10)
        cart_item = Cart(id=1, quantity=1, product_link=1, customer_link=1)
        db.session.add_all([product, cart_item])
        db.session.commit()
        response = client.get('/plus-cart?cart_id=1')  # Include cart_id in query string
        assert response.status_code == 200

def test_no_cart_id_provided(client):
    response = client.get('/plus-cart')  # No cart_id provided in the query string
    assert response.status_code == 400
    assert response.json == {'error': 'No cart ID provided'}
