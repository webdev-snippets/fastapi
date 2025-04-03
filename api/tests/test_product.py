import uuid
from . import *
from ..booking.models import Booking
from ..user.models import User


def test_create_booking(client: TestClient, session: Session, token: Token, user: User):
    datetime_now = datetime.now()
    response = client.post(
        f"/product",
        json={"title": f"Pixel 6 Pro",
              "description": "google Pixel 6 pro",
              "tags": ["google", "Pixel 6 Pro"],
              "image_path": "./assets/Pixel_6_pro.png"},
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )
    unauthenticated_response = client.post(
        f"/product",
        json={"title": f"Pixel 6 Pro",
              "description": "google Pixel 6 pro",
              "tags": ["google", "Pixel 6 Pro"],
              "image_path": "./assets/Pixel_6_pro.png"},
    )
    assert unauthenticated_response.status_code == 401

    _json = response.json()
    print(_json)
    _db_product: User = session.get(Product, uuid.UUID(_json['id']))

    assert response.status_code == 201
    assert _json is not None
    assert _json['title'] == "Pixel 6 Pro"
    assert _json['description'] == "google Pixel 6 pro"
    assert _json['tags'][0] == "google"
    assert _json['tags'][1] == "Pixel 6 Pro"
    assert _json['image_path'] == "./assets/Pixel_6_pro.png"
    assert _json['id'] is not None

    assert _db_product is not None
    assert _db_product.title == _json['title']
    assert _db_product.description == _json['description']
    assert _db_product.tags == _json['tags']
    assert _db_product.image_path == _json['image_path']
    assert str(_db_product.id) == _json['id']


def test_update_booking(client: TestClient, session: Session, token: Token, product: Product):
    response = client.patch(
        f"/product/{product.id}",
        json={"title": f"Pixel 9 Pro",
              "description": "google Pixel 9 pro",
              "tags": ["google", "Pixel 9 Pro",],
              "image_path": "./assets/Pixel_9_pro.png"},
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )

    unauthenticated_response = client.patch(
        f"/product/{product.id}",
        json={"title": f"Pixel 9 Pro",
              "description": "google Pixel 9 pro",
              "tags": ["google", "Pixel 9 Pro",],
              "image_path": "./assets/Pixel_9_pro.png"},
    )
    assert unauthenticated_response.status_code == 401
    _json = response.json()

    _db_product: User = session.get(Product, uuid.UUID(_json['id']))

    assert response.status_code == 200
    assert _json is not None
    assert _json['title'] == "Pixel 9 Pro"
    assert _json['description'] == "google Pixel 9 pro"
    assert _json['tags'][0] == "google"
    assert _json['tags'][1] == "Pixel 9 Pro"
    assert _json['image_path'] == "./assets/Pixel_9_pro.png"
    assert _json['id'] is not None

    assert _db_product is not None
    assert _db_product.title == _json['title']
    assert _db_product.description == _json['description']
    assert _db_product.tags == _json['tags']
    assert _db_product.image_path == _json['image_path']
    assert str(_db_product.id) == _json['id']


def test_get_booking(client: TestClient, session: Session, token: Token, product: Product):
    response = client.get(
        "/product",
    )
    _json = response.json()[0]
    print(_json)

    assert response.status_code == 200
    assert _json is not None
    assert _json['title'] == product.title
    assert _json['description'] == product.description
    assert _json['tags'][0] == product.tags[0]
    assert _json['tags'][1] == product.tags[1]
    assert _json['image_path'] == product.image_path
    assert _json['id'] == str(product.id)


def test_delete_booking(client: TestClient, session: Session, product: Product, token: Token):
    response = client.delete(
        f"/product/{product.id}",
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )

    unauthenticated_response = client.delete(
        "/product/{product.id}",
    )
    assert unauthenticated_response.status_code == 401

    _db_product: User = session.get(Product, product.id)

    assert response.status_code == 204

    assert _db_product is None
