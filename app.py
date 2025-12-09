from datetime import UTC, datetime

from flask import abort, Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hostel.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Use a stronger secret key in production; required for flashing messages
app.config["SECRET_KEY"] = "dev-secret-key"

# Prevent objects from expiring on commit so test fixtures stay usable.
db = SQLAlchemy(app, session_options={"expire_on_commit": False})


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=1)
    residents = db.relationship("Resident", backref="room", lazy="dynamic")

    @property
    def occupied(self) -> int:
        return self.residents.count()

    @property
    def has_space(self) -> bool:
        return self.occupied < self.capacity


class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    check_in = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    room_id = db.Column(db.Integer, db.ForeignKey("room.id"))


with app.app_context():
    db.create_all()


@app.context_processor
def inject_counts():
    room_count = Room.query.count()
    resident_count = Resident.query.count()
    return {"room_count": room_count, "resident_count": resident_count}


@app.route("/")
def dashboard():
    rooms = Room.query.order_by(Room.name).all()
    recent_residents = Resident.query.order_by(Resident.check_in.desc()).limit(5).all()
    return render_template("index.html", rooms=rooms, recent_residents=recent_residents)


@app.route("/rooms", methods=["GET", "POST"])
def rooms():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        capacity = request.form.get("capacity", "").strip()

        if not name:
            flash("Room name is required.", "error")
            return redirect(url_for("rooms"))

        try:
            capacity_val = int(capacity)
            if capacity_val <= 0:
                raise ValueError()
        except ValueError:
            flash("Capacity must be a positive number.", "error")
            return redirect(url_for("rooms"))

        if Room.query.filter_by(name=name).first():
            flash("Room name must be unique.", "error")
            return redirect(url_for("rooms"))

        db.session.add(Room(name=name, capacity=capacity_val))
        db.session.commit()
        flash(f"Room '{name}' added.", "success")
        return redirect(url_for("rooms"))

    rooms_list = Room.query.order_by(Room.name).all()
    return render_template("rooms.html", rooms=rooms_list)


@app.route("/rooms/<int:room_id>/delete", methods=["POST"])
def delete_room(room_id: int):
    room = db.session.get(Room, room_id)
    if room is None:
        abort(404)
    if room.residents.count() > 0:
        flash("Cannot delete a room that currently has residents.", "error")
        return redirect(url_for("rooms"))

    db.session.delete(room)
    db.session.commit()
    flash(f"Room '{room.name}' deleted.", "success")
    return redirect(url_for("rooms"))


@app.route("/residents", methods=["GET", "POST"])
def residents():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        room_id = request.form.get("room_id")

        if not full_name:
            flash("Resident name is required.", "error")
            return redirect(url_for("residents"))

        room = db.session.get(Room, room_id) if room_id else None
        if room is None:
            flash("Please select a valid room.", "error")
            return redirect(url_for("residents"))

        if not room.has_space:
            flash("Selected room is full. Choose another room.", "error")
            return redirect(url_for("residents"))

        resident = Resident(full_name=full_name, email=email, phone=phone, room=room)
        db.session.add(resident)
        db.session.commit()
        flash(f"{full_name} checked into {room.name}.", "success")
        return redirect(url_for("residents"))

    rooms_list = Room.query.order_by(Room.name).all()
    residents_list = (
        Resident.query.order_by(Resident.check_in.desc())
        .join(Room, isouter=True)
        .add_entity(Room)
        .all()
    )
    return render_template(
        "residents.html", residents=residents_list, rooms=rooms_list
    )


@app.route("/residents/<int:resident_id>/checkout", methods=["POST"])
def checkout_resident(resident_id: int):
    resident = db.session.get(Resident, resident_id)
    if resident is None:
        abort(404)
    name = resident.full_name
    db.session.delete(resident)
    db.session.commit()
    flash(f"{name} has been checked out.", "success")
    return redirect(url_for("residents"))


def init_db():
    # Ensure tables exist before first request
    with app.app_context():
        db.create_all()


if __name__ == "__main__":  # pragma: no cover
    init_db()
    app.run(debug=True)