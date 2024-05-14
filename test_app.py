import pytest
from app import app, generate_short_id
import psycopg2
import os

# Create a test client for the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test the add_url route
def test_add_url(client):
    # Test the GET request
    response = client.get('/add')
    assert response.status_code == 200

    # Test the POST request with a valid URL
    data = {'url': 'https://example.com'}
    response = client.post('/add', data=data, follow_redirects=True)
    assert b'Shortcut created' in response.data

    # Test the POST request with an invalid URL
    data = {'url': ''}
    response = client.post('/add', data=data, follow_redirects=True)
    assert b'Please enter a valid URL' in response.data

# Test the redirect_url route
def test_redirect_url(client):
    # Test with a valid short_id
    short_id = generate_short_id()
    url = 'https://example.com'
    app.url_mapping[short_id] = url
    response = client.get(f'/{short_id}')
    assert response.status_code == 200
    assert url.encode() in response.data

    # Test with an invalid short_id
    response = client.get('/invalid_id')
    assert response.status_code == 404
    assert b'URL not found' in response.data

# Test the display_shortcuts route
def test_display_shortcuts(client):
    # Connect to the test database
    conn = psycopg2.connect(
        host=os.environ.get('TEST_DB_HOST'),
        database=os.environ.get('TEST_DB_NAME'),
        user=os.environ.get('TEST_DB_USER'),
        password=os.environ.get('TEST_DB_PASSWORD')
    )

    # Insert some test data
    cur = conn.cursor()
    cur.execute("INSERT INTO shortcuts (shortcut, url) VALUES (%s, %s)", ('abc123', 'https://example.com'))
    conn.commit()
    cur.close()

    # Test the display_shortcuts route
    response = client.get('/shortcuts')
    assert response.status_code == 200
    assert b'abc123' in response.data
    assert b'https://example.com' in response.data

    # Clean up the test data
    cur = conn.cursor()
    cur.execute("DELETE FROM shortcuts")
    conn.commit()
    cur.close()
    conn.close()
