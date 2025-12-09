from app import Room, db


def test_add_room_success(client):
    resp = client.post("/rooms", data={"name": "B201", "capacity": "3"}, follow_redirects=True)
    assert resp.status_code == 200
    with client.application.app_context():
        room = Room.query.filter_by(name="B201").first()
        assert room is not None
        assert room.capacity == 3


def test_add_room_requires_name(client):
    resp = client.post("/rooms", data={"name": "", "capacity": "2"}, follow_redirects=True)
    assert resp.status_code == 200
    assert Room.query.count() == 0


def test_add_room_requires_positive_capacity(client):
    resp = client.post("/rooms", data={"name": "X1", "capacity": "0"}, follow_redirects=True)
    assert resp.status_code == 200
    assert Room.query.filter_by(name="X1").first() is None


def test_add_room_rejects_duplicate(client, room):
    resp = client.post("/rooms", data={"name": room.name, "capacity": "2"}, follow_redirects=True)
    assert resp.status_code == 200
    with client.application.app_context():
        count = Room.query.filter_by(name=room.name).count()
        assert count == 1


def test_delete_room_blocked_when_occupied(client, room, resident):
    resp = client.post(f"/rooms/{room.id}/delete", follow_redirects=True)
    assert resp.status_code == 200
    with client.application.app_context():
        assert db.session.get(Room, room.id) is not None


def test_delete_room_after_checkout(client, room, resident):
    # First checkout resident to free room
    client.post(f"/residents/{resident.id}/checkout", follow_redirects=True)
    resp = client.post(f"/rooms/{room.id}/delete", follow_redirects=True)
    assert resp.status_code == 200
    with client.application.app_context():
        assert db.session.get(Room, room.id) is None

