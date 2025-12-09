import pytest

from app import app, db, Room, Resident


@pytest.fixture(autouse=True)
def _app_context():
    # Isolate each test in its own in-memory DB.
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def room():
    with app.app_context():
        room = Room(name="A101", capacity=2)
        db.session.add(room)
        db.session.commit()
        return room


@pytest.fixture
def resident(room):
    with app.app_context():
        res = Resident(full_name="Jane Doe", email="jane@example.com", room=room)
        db.session.add(res)
        db.session.commit()
        return res

