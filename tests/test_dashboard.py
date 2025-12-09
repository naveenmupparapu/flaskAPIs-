from app import Room, Resident, db


def test_dashboard_shows_counts(client):
    with client.application.app_context():
        room = Room(name="D101", capacity=2)
        db.session.add(room)
        db.session.add(Resident(full_name="Zoe", room=room))
        db.session.commit()

    resp = client.get("/")
    assert resp.status_code == 200
    html = resp.data.decode()
    assert "Rooms" in html
    assert "Residents" in html
    assert "D101" in html
    assert "Zoe" in html


def test_init_db_executes():
    # Drops happen in fixture; ensure init_db can recreate without error.
    from app import init_db

    init_db()

