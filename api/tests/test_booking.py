import uuid
from . import *
from ..booking.models import Booking
from ..user.models import User


def test_create_booking(client: TestClient, session: Session, token: Token, user: User):
    datetime_now = datetime.now()
    response = client.post(
        f"/booking",
        json={"time": f"{datetime_now}", "location": "68 opsrey drive",
              "notes": "testing", "booking_type": "installation"},
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )
    unauthenticated_response = client.post(
        f"/booking",
        json={"time": f"{datetime_now}", "location": "68 opsrey drive",
              "notes": "testing", "booking_type": "installation"},
    )
    assert unauthenticated_response.status_code == 401

    _json = response.json()
    print(_json)
    _db_booking: User = session.get(Booking, uuid.UUID(_json['id']))

    assert response.status_code == 201
    assert _json is not None
    assert _json['location'] == "68 opsrey drive"
    assert _json['notes'] == "testing"
    assert _json['booking_type'] == "installation"
    assert _json['time'] == str(datetime_now)
    assert _json['id'] is not None

    assert _db_booking is not None
    assert _db_booking.location == _json['location']
    assert _db_booking.time == _json['time']
    assert _db_booking.notes == _json['notes']
    assert _db_booking.booking_type == _json['booking_type']
    assert str(_db_booking.id) == _json['id']


def test_update_booking(client: TestClient, session: Session, token: Token, booking: Booking):
    response = client.patch(
        f"/booking/{booking.id}",
        json={"time": f"{datetime.now()}", "location": "68 opsrey drive",
              "notes": "testing"},
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )

    unauthenticated_response = client.patch(
        f"/booking/{booking.id}",
        json={"time": f"{datetime.now()}", "location": "68 opsrey drive",
              "notes": "testing"},
    )
    assert unauthenticated_response.status_code == 401
    _json = response.json()
    print(_json)

    _db_booking: Booking = session.get(Booking, uuid.UUID(_json['id']))

    assert response.status_code == 200
    assert _json is not None
    assert _json['location'] == "68 opsrey drive"
    assert _json['notes'] == "testing"
    assert _json['booking_type'] == "installation"
    assert _json['time'] is not None
    assert _json['id'] is not None

    assert _db_booking is not None
    assert _db_booking.location == _json['location']
    assert _db_booking.time == _json['time']
    assert _db_booking.notes == _json['notes']
    assert _db_booking.booking_type == _json['booking_type']
    assert str(_db_booking.id) == _json['id']


def test_get_booking(client: TestClient, session: Session, token: Token, booking: Booking):
    response = client.get(
        "/booking",
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )
    unauthenticated_response = client.get(
        "/booking"
    )
    assert unauthenticated_response.status_code == 401

    _json = response.json()[0]

    assert response.status_code == 200
    assert _json is not None
    assert _json['location'] == booking.location
    assert _json['time'] == booking.time
    assert _json['notes'] == booking.notes
    assert _json['booking_type'] == booking.booking_type
    assert _json['id'] == str(booking.id)


def test_delete_booking(client: TestClient, session: Session, booking: Booking, token: Token):
    response = client.delete(
        f"/booking/{booking.id}",
        headers={
            "Authorization": f"Bearer {token.access_token}"
        }
    )

    unauthenticated_response = client.delete(
        "/booking/{booking.id}",
    )
    assert unauthenticated_response.status_code == 401

    _db_booking: User = session.get(Booking, booking.id)

    assert response.status_code == 204

    assert _db_booking is None
