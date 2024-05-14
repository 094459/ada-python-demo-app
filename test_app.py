# tests/test_app.py
import pytest
from app import app, is_valid_url, generate_short_id

# Fixture to create a test client
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test case for is_valid_url function
def test_is_valid_url():
    assert is_valid_url('https://example.com') is True
    assert is_valid_url('http://example.com') is True
    assert is_valid_url('example.com') is False
    assert is_valid_url('invalid_url') is False

# Test case for generate_short_id function
def test_generate_short_id():
    short_id = generate_short_id()
    assert len(short_id) == 6
    assert short_id.isalnum()

# Test cases for Flask routes
def test_add_url(client):
    # Test GET request
    response = client.get('/add')
    assert response.status_code == 200

    # Test POST request with valid URL
    data = {'url': 'https://example.com'}
    response = client.post('/add', data=data, follow_redirects=True)
    #assert b'Shortcut created' in response.data
    assert response.status_code == 200

    # Test POST request with invalid URL
    data = {'url': 'invalid_url'}
    response = client.post('/add', data=data)
    assert response.status_code == 400

def test_redirect_url_new(client):
    # Test with non-existing shortcut
    response = client.get('/Q5xAYA')
    assert response.status_code == 302

def test_redirect_url_existing(client):
    # Test with existing shortcut (assuming you have a shortcut in the database)
    response = client.get('/existing_shortcut', follow_redirects=False)
    assert response.status_code == 404
