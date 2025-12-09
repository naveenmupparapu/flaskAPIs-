"""
Unit tests specifically for the Student model.
"""
import pytest
from datetime import datetime, date
from app import db, Student


class TestStudentModelAttributes:
    """Test Student model attribute types and constraints."""

    def test_id_is_primary_key(self, test_app):
        """Test that id is the primary key."""
        with test_app.app_context():
            student = Student(
                first_name='Test',
                last_name='User',
                email='test1@example.com',
                phone='1234567890',
                date_of_birth=date(2000, 1, 1),
                gender='Male',
                address='123 Test St',
                city='Test City',
                course='Computer Science'
            )
            db.session.add(student)
            db.session.commit()
            
            assert student.id == 1

    def test_id_auto_increments(self, test_app):
        """Test that id auto-increments."""
        with test_app.app_context():
            for i in range(3):
                student = Student(
                    first_name=f'Test{i}',
                    last_name='User',
                    email=f'test{i}@example.com',
                    phone=f'123456789{i}',
                    date_of_birth=date(2000, 1, 1),
                    gender='Male',
                    address='123 Test St',
                    city='Test City',
                    course='Computer Science'
                )
                db.session.add(student)
            db.session.commit()
            
            students = Student.query.all()
            assert len(students) == 3
            assert students[0].id < students[1].id < students[2].id

    def test_registration_date_default(self, test_app):
        """Test that registration_date has a default value."""
        with test_app.app_context():
            before = datetime.utcnow()
            
            student = Student(
                first_name='Test',
                last_name='User',
                email='test_date@example.com',
                phone='1234567890',
                date_of_birth=date(2000, 1, 1),
                gender='Male',
                address='123 Test St',
                city='Test City',
                course='Computer Science'
            )
            db.session.add(student)
            db.session.commit()
            
            after = datetime.utcnow()
            
            assert student.registration_date is not None
            assert before <= student.registration_date <= after

    def test_email_uniqueness(self, test_app):
        """Test that email must be unique."""
        with test_app.app_context():
            student1 = Student(
                first_name='First',
                last_name='User',
                email='unique@example.com',
                phone='1234567890',
                date_of_birth=date(2000, 1, 1),
                gender='Male',
                address='123 Test St',
                city='Test City',
                course='Computer Science'
            )
            db.session.add(student1)
            db.session.commit()
            
            student2 = Student(
                first_name='Second',
                last_name='User',
                email='unique@example.com',
                phone='0987654321',
                date_of_birth=date(2001, 2, 2),
                gender='Female',
                address='456 Test Ave',
                city='Another City',
                course='Business Administration'
            )
            db.session.add(student2)
            
            with pytest.raises(Exception):
                db.session.commit()


class TestStudentModelQueries:
    """Test various query operations on Student model."""

    def test_query_all(self, test_app):
        """Test querying all students."""
        with test_app.app_context():
            for i in range(5):
                student = Student(
                    first_name=f'Student{i}',
                    last_name='Test',
                    email=f'student{i}@example.com',
                    phone=f'123456789{i}',
                    date_of_birth=date(2000, 1, 1),
                    gender='Male',
                    address='123 Test St',
                    city='Test City',
                    course='Computer Science'
                )
                db.session.add(student)
            db.session.commit()
            
            all_students = Student.query.all()
            assert len(all_students) == 5

    def test_query_filter_by_course(self, test_app):
        """Test filtering students by course."""
        with test_app.app_context():
            courses = ['Computer Science', 'Medicine', 'Computer Science']
            for i, course in enumerate(courses):
                student = Student(
                    first_name=f'Student{i}',
                    last_name='Test',
                    email=f'course_test{i}@example.com',
                    phone=f'123456789{i}',
                    date_of_birth=date(2000, 1, 1),
                    gender='Male',
                    address='123 Test St',
                    city='Test City',
                    course=course
                )
                db.session.add(student)
            db.session.commit()
            
            cs_students = Student.query.filter_by(course='Computer Science').all()
            assert len(cs_students) == 2

    def test_query_filter_by_gender(self, test_app):
        """Test filtering students by gender."""
        with test_app.app_context():
            genders = ['Male', 'Female', 'Male', 'Other']
            for i, gender in enumerate(genders):
                student = Student(
                    first_name=f'Student{i}',
                    last_name='Test',
                    email=f'gender_test{i}@example.com',
                    phone=f'123456789{i}',
                    date_of_birth=date(2000, 1, 1),
                    gender=gender,
                    address='123 Test St',
                    city='Test City',
                    course='Computer Science'
                )
                db.session.add(student)
            db.session.commit()
            
            male_students = Student.query.filter_by(gender='Male').all()
            assert len(male_students) == 2

    def test_query_order_by_registration_date(self, test_app):
        """Test ordering students by registration date."""
        with test_app.app_context():
            for i in range(3):
                student = Student(
                    first_name=f'Student{i}',
                    last_name='Test',
                    email=f'order_test{i}@example.com',
                    phone=f'123456789{i}',
                    date_of_birth=date(2000, 1, 1),
                    gender='Male',
                    address='123 Test St',
                    city='Test City',
                    course='Computer Science'
                )
                db.session.add(student)
                db.session.commit()
            
            students = Student.query.order_by(Student.registration_date.desc()).all()
            assert students[0].first_name == 'Student2'
            assert students[2].first_name == 'Student0'

    def test_query_first(self, test_app):
        """Test getting first student."""
        with test_app.app_context():
            for i in range(3):
                student = Student(
                    first_name=f'Student{i}',
                    last_name='Test',
                    email=f'first_test{i}@example.com',
                    phone=f'123456789{i}',
                    date_of_birth=date(2000, 1, 1),
                    gender='Male',
                    address='123 Test St',
                    city='Test City',
                    course='Computer Science'
                )
                db.session.add(student)
            db.session.commit()
            
            first_student = Student.query.first()
            assert first_student is not None
            assert first_student.first_name == 'Student0'

    def test_query_get_by_id(self, test_app):
        """Test getting student by ID."""
        with test_app.app_context():
            student = Student(
                first_name='GetById',
                last_name='Test',
                email='getbyid@example.com',
                phone='1234567890',
                date_of_birth=date(2000, 1, 1),
                gender='Male',
                address='123 Test St',
                city='Test City',
                course='Computer Science'
            )
            db.session.add(student)
            db.session.commit()
            
            student_id = student.id
            fetched = Student.query.get(student_id)
            assert fetched is not None
            assert fetched.first_name == 'GetById'

    def test_query_count(self, test_app):
        """Test counting students."""
        with test_app.app_context():
            for i in range(7):
                student = Student(
                    first_name=f'Student{i}',
                    last_name='Test',
                    email=f'count_test{i}@example.com',
                    phone=f'123456789{i}',
                    date_of_birth=date(2000, 1, 1),
                    gender='Male',
                    address='123 Test St',
                    city='Test City',
                    course='Computer Science'
                )
                db.session.add(student)
            db.session.commit()
            
            count = Student.query.count()
            assert count == 7


class TestStudentModelDateHandling:
    """Test date handling in Student model."""

    def test_date_of_birth_stored_correctly(self, test_app):
        """Test that date of birth is stored correctly."""
        with test_app.app_context():
            test_dob = date(1995, 6, 15)
            student = Student(
                first_name='Date',
                last_name='Test',
                email='date_test@example.com',
                phone='1234567890',
                date_of_birth=test_dob,
                gender='Male',
                address='123 Test St',
                city='Test City',
                course='Computer Science'
            )
            db.session.add(student)
            db.session.commit()
            
            fetched = Student.query.filter_by(email='date_test@example.com').first()
            assert fetched.date_of_birth == test_dob
            assert fetched.date_of_birth.year == 1995
            assert fetched.date_of_birth.month == 6
            assert fetched.date_of_birth.day == 15

    def test_leap_year_date(self, test_app):
        """Test handling of leap year dates."""
        with test_app.app_context():
            test_dob = date(2000, 2, 29)  # Leap year
            student = Student(
                first_name='Leap',
                last_name='Year',
                email='leap@example.com',
                phone='1234567890',
                date_of_birth=test_dob,
                gender='Female',
                address='123 Test St',
                city='Test City',
                course='Computer Science'
            )
            db.session.add(student)
            db.session.commit()
            
            fetched = Student.query.filter_by(email='leap@example.com').first()
            assert fetched.date_of_birth == test_dob








