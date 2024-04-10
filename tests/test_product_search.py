import pytest
from flask import url_for, json
from website import create_app, db
from website.models import Product
from website import create_app

@pytest.fixture
def client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': "sqlite:///:memory:"})
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            product1 = Product(
                product_name='Test Product 1', 
                current_price=50.0, 
                previous_price=45.0,  # Add this
                product_picture='test1.jpg', 
                in_stock=10
            )
            product2 = Product(
                product_name='Test Product 2', 
                current_price=100.0, 
                previous_price=90.0,  # And this
                product_picture='test2.jpg', 
                in_stock=0
            )
            db.session.query(Product).delete()
            db.session.add(product1)
            db.session.add(product2)
            db.session.commit()
            # Setup initial data here...
        yield client


def test_search_results_found(client):
    response = client.post('/productsearch', data={'search': 'Test', 'min_price': '10', 'max_price': '100'})
    data = json.loads(response.data)
    assert len(data['results']) > 0
    assert all('Test' in product['product_name'] for product in data['results'])

def test_no_search_results_found(client):
    response = client.post('/productsearch', data={'search': 'Nonexistent', 'min_price': '10', 'max_price': '100'})
    data = json.loads(response.data)
    assert len(data['results']) == 0

def test_get_request_returns_all_products(client):
    response = client.get('/productsearch')
    data = json.loads(response.data)
    assert len(data['results']) == 2
    assert data['results'][0]['product_name'] == 'Test Product 1'
    assert data['results'][1]['product_name'] == 'Test Product 2'
def test_search_results_filtered_by_price_range(client):
    response = client.post('/productsearch', data={'min_price': '10', 'max_price': '50'})
    data = json.loads(response.data)
    assert len(data['results']) == 1
    assert data['results'][0]['product_name'] == 'Test Product 1'
    assert data['results'][0]['price'] == 50.0