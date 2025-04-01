from . import *

def test_token(client: TestClient, user: User):
    response =  client.post(
        "/auth/token", 
        data={"username": f"{user.username}", "password": "Password1", "scope": "user user:write user:delete", "grant_type": "password"}
    )
    _json = response.json()

    assert 'access_token' in _json
    assert 'token_type' in _json
    assert _json['token_type'] == "bearer"