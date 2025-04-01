import pytest
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from datetime import timedelta, datetime

from .. import app, get_session
from ..user.models import User
from ..booking.models import Booking
from ..auth.models import Token
from ..user.utils import hash_password
from ..auth.utils import create_access_token
from ..config import Settings, SCOPES


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app, raise_server_exceptions=True)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="user")
def user_fixture(session: Session) -> User:
    u = User(
        username="tester",
        email="tester@example.com",
        password=hash_password("Password1")
    )
    session.add(u)
    session.commit()
    session.refresh(u)
    return u


@pytest.fixture(name="booking")
def booking_fixture(session: Session, user: User) -> Booking:
    b = Booking(
        user_id=user.id,
        time=str(datetime.now()),
        location="London",
        notes="test notes",
        booking_type="installation"
    )
    session.add(b)
    session.commit()
    session.refresh(b)
    return b


@pytest.fixture(name="token")
def token_fixture(session: Session, user: User) -> Token:
    # print(f"{' '.join(SCOPES.keys())}")
    token = create_access_token(
        {"sub": f"{str(user.id)}", "scopes": f"{' '.join(SCOPES.keys())}"}, timedelta(minutes=5))
    return Token(access_token=token, token_type="Bearer")
