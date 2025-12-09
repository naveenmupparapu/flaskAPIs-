<<<<<<< HEAD
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

=======
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'student-registration-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'
>>>>>>> 739b3dfda79936a2a5228c79b39e64d5c3f282ea

with app.app_context():
    db.create_all()

<<<<<<< HEAD

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
=======
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        dob_str = request.form['date_of_birth']
        gender = request.form['gender']
        address = request.form['address']
        city = request.form['city']
        course = request.form['course']

        date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()

        existing_student = Student.query.filter_by(email=email).first()
        if existing_student:
            flash('A student with this email already exists!', 'error')
            return redirect(url_for('index'))

        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            city=city,
            course=course
        )

        db.session.add(new_student)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('success', student_id=new_student.id))

    except Exception as e:
        flash(f'Registration failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/success/<int:student_id>')
def success(student_id):
    student = Student.query.get_or_404(student_id)
    is_update = request.args.get('updated') == '1'
    return render_template('success.html', student=student, is_update=is_update)

@app.route('/students')
def students():
    all_students = Student.query.order_by(Student.registration_date.desc()).all()
    return render_template('students.html', students=all_students)

@app.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('students'))

@app.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        try:
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            phone = request.form['phone']
            dob_str = request.form['date_of_birth']
            gender = request.form['gender']
            address = request.form['address']
            city = request.form['city']
            course = request.form['course']

            date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()

            existing_student = Student.query.filter(
                Student.email == email,
                Student.id != student_id
            ).first()
            if existing_student:
                flash('A student with this email already exists!', 'error')
                return redirect(url_for('edit_student', student_id=student_id))

            student.first_name = first_name
            student.last_name = last_name
            student.email = email
            student.phone = phone
            student.date_of_birth = date_of_birth
            student.gender = gender
            student.address = address
            student.city = city
            student.course = course

            db.session.commit()

            flash('Student updated successfully!', 'success')
            return redirect(url_for('success', student_id=student.id, updated=1))
        except Exception as e:
            flash(f'Update failed: {str(e)}', 'error')
            return redirect(url_for('edit_student', student_id=student_id))

    return render_template('edit_student.html', student=student)

if __name__ == '__main__':  # pragma: no cover
    app.run(debug=True, port=5000)

>>>>>>> 739b3dfda79936a2a5228c79b39e64d5c3f282ea
