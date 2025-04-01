import uuid
from . import *
from ..user.models import User

def test_create_user(client: TestClient, session: Session):
    response =  client.post(
        "/user", 
        json={"username": "test", "email": "test@example.com", "password": "test"}
    )
    _json = response.json()
    _db_user: User = session.get(User, uuid.UUID(_json['id']))

    assert response.status_code == 201
    assert _json is not None
    assert _json['username'] == "test"
    assert _json['email'] == "test@example.com"
    assert _json['id'] is not None

    assert _db_user is not None
    assert _db_user.username == _json['username']
    assert _db_user.email == _json['email']
    assert str(_db_user.id) == _json['id']
    assert _db_user.password is not None


def test_update_user(client: TestClient, session: Session, token: Token):
    response =  client.patch(
        "/user", 
        json={"username": "testupdate", "email": "testupdate@example.com", "password": "testupdate"},
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )

    unauthenticated_response =  client.patch(
        "/user", 
        json={"username": "testupdate", "email": "testupdate@example.com", "password": "testupdate"},
    )
    assert unauthenticated_response.status_code == 401
    _json = response.json()

    _db_user: User = session.get(User, uuid.UUID(_json['id']))

    assert response.status_code == 200
    assert _json is not None
    assert _json['username'] == "testupdate"
    assert _json['email'] == "testupdate@example.com"
    assert _json['id'] is not None

    assert _db_user is not None
    assert _db_user.username == _json['username']
    assert _db_user.email == _json['email']
    assert str(_db_user.id) == _json['id']
    assert _db_user.password is not None

def test_get_user(client: TestClient, session: Session, token: Token):
    response =  client.get(
        "/user", 
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )
    unauthenticated_response =  client.get(
        "/user"
    )
    assert unauthenticated_response.status_code == 401

    _json = response.json()
    _db_user: User = session.get(User, uuid.UUID(_json['id']))

    assert response.status_code == 200
    assert _json is not None
    assert _json['username'] == _db_user.username
    assert _json['email'] == _db_user.email
    assert _json['id'] == str(_db_user.id)


def test_delete_user(client: TestClient, session: Session,user: User, token: Token):
    response =  client.delete(
        "/user", 
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )

    unauthenticated_response =  client.patch(
        "/user", 
        )
    assert unauthenticated_response.status_code == 401

    _db_user: User = session.get(User, user.id)

    assert response.status_code == 204

    assert _db_user is None
