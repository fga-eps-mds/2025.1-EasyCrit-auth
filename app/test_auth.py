import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User
from app.database.database import SessionLocal

client = TestClient(app)


@pytest.fixture(scope='module')
def test_user():
  db = SessionLocal()

  user = db.query(User).filter(User.username == 'testuser').first()
  if not user:
    user = User(username='testuser', email='test@example.com', password='testpassword')
    db.add(user)
    db.commit()
    db.refresh(user)
  yield user

  db.delete(user)
  db.commit()
  db.close()


def test_login_success(test_user):
  response = client.post('/auth/login', json={'username': 'testuser', 'password': 'testpassword'})
  assert response.status_code == 200
  data = response.json()
  assert 'access_token' in data
  assert data['type'].lower() == 'bearer'


def test_login_wrong_password(test_user):
  response = client.post('/auth/login', json={'username': 'testuser', 'password': 'wrongpassword'})
  assert response.status_code == 401
  assert response.json() == {'detail': 'Incorrect user or password'}


def test_login_nonexistent_user():
  response = client.post('/auth/login', json={'username': 'nonexistentuser', 'password': 'somepassword'})
  assert response.status_code == 401
  assert response.json() == {'detail': 'Incorrect user or password'}


def test_login_missing_username():
  response = client.post('/auth/login', json={'password': 'testpassword'})
  assert response.status_code == 422
  data = response.json()
  assert data['detail'][0]['type'] == 'missing'
  assert data['detail'][0]['loc'] == ['body', 'username']
  assert data['detail'][0]['msg'] == 'Field required'


def test_login_missing_password():
  response = client.post('/auth/login', json={'username': 'testuser'})
  assert response.status_code == 422
  data = response.json()
  assert data['detail'][0]['type'] == 'missing'
  assert data['detail'][0]['loc'] == ['body', 'password']
  assert data['detail'][0]['msg'] == 'Field required'
