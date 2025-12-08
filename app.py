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

with app.app_context():
    db.create_all()

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
    return render_template('success.html', student=student)

@app.route('/students')
def students():
    all_students = Student.query.order_by(Student.registration_date.desc()).all()
    return render_template('students.html', students=all_students)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

