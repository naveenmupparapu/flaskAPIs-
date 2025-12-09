from app import Resident, Room, db


def test_check_in_resident(client, room):
    resp = client.post(
        "/residents",
        data={
            "full_name": "John Smith",
            "email": "john@example.com",
            "phone": "123",
            "room_id": room.id,
        },
        follow_redirects=True,
    )
    assert resp.status_code == 200
    with client.application.app_context():
        res = Resident.query.filter_by(full_name="John Smith").first()
        assert res is not None
        assert res.room_id == room.id


def test_check_in_requires_name(client, room):
    resp = client.post(
        "/residents",
        data={"full_name": "", "room_id": room.id},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    with client.application.app_context():
        assert Resident.query.count() == 0


def test_check_in_requires_valid_room(client):
    resp = client.post(
        "/residents",
        data={"full_name": "No Room", "room_id": 9999},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    with client.application.app_context():
        assert Resident.query.filter_by(full_name="No Room").first() is None


def test_check_in_rejected_when_room_full(client):
    with client.application.app_context():
        small_room = Room(name="C101", capacity=1)
        db.session.add(small_room)
        db.session.add(Resident(full_name="Alice", room=small_room))
        db.session.commit()
        room_id = small_room.id

    resp = client.post(
        "/residents",
        data={"full_name": "Bob", "room_id": room_id},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    with client.application.app_context():
        res_count = Resident.query.filter_by(room_id=room_id).count()
        assert res_count == 1  # still only Alice


def test_checkout_removes_resident(client, room, resident):
    resp = client.post(f"/residents/{resident.id}/checkout", follow_redirects=True)
    assert resp.status_code == 200
    with client.application.app_context():
        assert db.session.get(Resident, resident.id) is None

