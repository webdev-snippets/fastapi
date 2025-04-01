from . import *

def test_status(client: TestClient):
    response = client.get("/status")
    _json = response.json()

    assert _json is not None
    assert _json['status'] == "ok"


def test_health(client: TestClient):
    response = client.get("/health")
    _json = response.json()


    assert response.status_code == 200
    assert _json is not None
    assert _json['status'] == "ok"
    assert _json['db_url'] is not None
    assert _json['issuer'] is not None
    assert _json['expire_time'] is not None
    assert _json['debug_level'] is not None
