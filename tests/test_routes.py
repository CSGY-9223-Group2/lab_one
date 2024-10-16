import pytest
from app import app, db, User, Paste, bcrypt
import jwt
import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def generate_test_token(user_id):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def test_register_route(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 201
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    print("test_register_route passed")  # Confirmation message for GitHub Actions

def test_login_route(client):
    password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    new_user = User(username='testuser', password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password123'
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert 'token' in json_data
    print("test_login_route passed")  # Confirmation message for GitHub Actions

def test_create_paste_route(client):
    password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    new_user = User(username='testuser', password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    token = generate_test_token(new_user.id)

    response = client.post('/create_paste', json={
        'content': 'Test paste content',
        'public': True
    }, headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 201
    json_data = response.get_json()
    assert 'paste_id' in json_data
    paste = Paste.query.filter_by(id=json_data['paste_id']).first()
    assert paste is not None
    assert paste.content == 'Test paste content'
    print("test_create_paste_route passed")  # Confirmation message for GitHub Actions

def test_my_pastes_route(client):
    password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    new_user = User(username='testuser', password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    token = generate_test_token(new_user.id)

    paste1 = Paste(content='Private paste', public=False, owner=new_user)
    paste2 = Paste(content='Public paste', public=True, owner=new_user)
    db.session.add(paste1)
    db.session.add(paste2)
    db.session.commit()

    response = client.get('/my_pastes', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data['user_pastes']) == 2  # The user should see both public and private pastes
    print("test_my_pastes_route passed")  # Confirmation message for GitHub Actions

def test_edit_paste_route(client):
    password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    new_user = User(username='testuser', password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    token = generate_test_token(new_user.id)

    paste = Paste(content='Original paste content', public=True, owner=new_user)
    db.session.add(paste)
    db.session.commit()

    response = client.put(f'/edit_paste/{paste.id}', json={
        'content': 'Updated paste content',
        'public': False
    }, headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'Paste updated successfully'
    updated_paste = Paste.query.get(paste.id)
    assert updated_paste.content == 'Updated paste content'
    assert not updated_paste.public
    print("test_edit_paste_route passed")  # Confirmation message for GitHub Actions

def test_delete_paste_route(client):
    password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    new_user = User(username='testuser', password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    token = generate_test_token(new_user.id)

    paste = Paste(content='Paste to delete', public=True, owner=new_user)
    db.session.add(paste)
    db.session.commit()

    response = client.delete(f'/delete_paste/{paste.id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'Paste deleted successfully'

    deleted_paste = Paste.query.get(paste.id)
    assert deleted_paste is None
    print("test_delete_paste_route passed")  # Confirmation message for GitHub Actions

# Test: Try to register the same user twice and detect the error
# Expected output: The second attempt should return a 400 status code with a message "User already exists"
def test_register_duplicate_user(client):
    response = client.post('/register', json={
        'username': 'duplicateuser',
        'password': 'password123'
    })
    assert response.status_code == 201  # First registration succeeds

    # Try registering the same user again
    duplicate_response = client.post('/register', json={
        'username': 'duplicateuser',
        'password': 'password123'
    })
    
    assert duplicate_response.status_code == 400
    json_data = duplicate_response.get_json()
    assert json_data['error'] == 'User already exists'
    print("test_register_duplicate_user passed")

# Test: Try to edit a paste which does not exist
# Expected output: Should return a 404 status code with description "Paste not found"
def test_edit_nonexistent_paste(client):
    password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    new_user = User(username='testuser', password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    token = generate_test_token(new_user.id)

    # Attempt to edit a paste that does not exist (id 9999)
    response = client.put('/edit_paste/9999', json={
        'content': 'Updated content',
        'public': True
    }, headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 404
    json_data = response.get_json(silent=True)
    assert json_data is not None, "Expected JSON response, but got None"
    assert response.json.get('description') == 'Paste not found'
    print("test_edit_nonexistent_paste passed")

# Test: Try to delete a paste which does not exist
# Expected output: Should return a 404 status code with description "Paste not found"
def test_delete_nonexistent_paste(client):
    password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    new_user = User(username='testuser', password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    token = generate_test_token(new_user.id)

    # Attempt to delete a paste that does not exist (id 9999)
    response = client.delete('/delete_paste/9999', headers={'Authorization': f'Bearer {token}'})
    
    assert response.status_code == 404
    json_data = response.get_json(silent=True)
    assert json_data is not None, "Expected JSON response, but got None"
    assert response.json.get('description') == 'Paste not found'
    print("test_delete_nonexistent_paste passed")

# Test: Try to login with the wrong password
# Expected output: Should return a 401 status code with description "Invalid username or password"
def test_login_wrong_password(client):
    password_hash = bcrypt.generate_password_hash('password123').decode('utf-8')
    new_user = User(username='testuser', password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()

    # Attempt to login with the wrong password
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    json_data = response.get_json(silent=True)
    assert json_data is not None, "Expected JSON response, but got None"
    assert response.json.get('description') == 'Invalid username or password'
    print("test_login_wrong_password passed")
 