# tests/test_routes.py
import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Set up database for testing
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_register_route(client):
    # Simulate a post request to /register
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    # Check if the status code is 201 (Created)
    assert response.status_code == 201
    
    # Check if the user was added to the database
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.username == 'testuser'
