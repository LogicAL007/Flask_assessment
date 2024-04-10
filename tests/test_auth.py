import pytest
from flask import Flask
from app.models import Customer
from app import db
from app.auth import change_password
from unittest.mock import patch
from flask import url_for
from app import create_app
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

@pytest.fixture(scope='module')
def init_database(app):
    
    with app.app_context():
        db.create_all()
        user = Customer(email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        yield  


class TestSignUp:
    def test_valid_account_creation(self, client):
        data = {'email': 'test@example.com', 'username': 'test_user', 'password1': 'password123', 'password2': 'password123'}
        response = client.post('/sign-up', json=data)
        assert response.status_code == 201
        assert response.json == {'message': 'Account created successfully'}

    def test_minimum_length_account_creation(self, client):
        data = {'email': 'a@a.com', 'username': 'adddddd', 'password1': 'addddd', 'password2': 'addddd'}
        response = client.post('/sign-up', json=data)
        assert response.status_code == 201
        assert response.json == {'message': 'Account created successfully'}

    def test_missing_required_fields(self, client):
        data = {'email': 'test@example.com', 'username': '', 'password1': 'password123', 'password2': 'password123'}
        response = client.post('/sign-up', json=data)
        assert response.status_code == 400
        assert response.json == {'error': 'All fields are required'}

    def test_passwords_do_not_match(self, client):
        data = {'email': 'test@example.com', 'username': 'test_user', 'password1': 'password123', 'password2': 'password456'}
        response = client.post('/sign-up', json=data)
        assert response.status_code == 400
        assert response.json == {'error': 'Passwords do not match'}

class TestLogin:
    def test_valid_email_and_password(self, client):
        response = client.post('/login', json={'email': 'test@example.com', 'password': 'password'})
        assert response.status_code == 200
        assert response.get_json() == {'message': 'Login successful'}

    def test_sql_injection(self, client):
        response = client.post('/login', json={'email': "'; DROP TABLE Customer; --", 'password': "'; DROP TABLE Customer; --"})
        assert response.status_code == 401
        assert response.get_json() == {'error': 'Invalid email or password'}
