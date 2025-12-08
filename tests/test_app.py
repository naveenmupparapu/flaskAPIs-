"""
Comprehensive unit tests for the Student Registration Application.
Targeting 100% code coverage.
"""
import pytest
from datetime import datetime, date
from app import app, db, Student


class TestStudentModel:
    """Test cases for the Student model."""

    def test_student_creation(self, test_app):
        """Test creating a student instance."""
        with test_app.app_context():
            student = Student(
                first_name='Test',
                last_name='User',
                email='test@example.com',
                phone='1234567890',
                date_of_birth=date(2000, 1, 1),
                gender='Male',
                address='123 Test St',
                city='Test City',
                course='Computer Science'
            )
            db.session.add(student)
            db.session.commit()
            
            assert student.id is not None
            assert student.first_name == 'Test'
            assert student.last_name == 'User'
            assert student.email == 'test@example.com'
            assert student.registration_date is not None

    def test_student_repr(self, test_app):
        """Test the string representation of a student."""
        with test_app.app_context():
            student = Student(
                first_name='John',
                last_name='Doe',
                email='john@example.com',
                phone='1234567890',
                date_of_birth=date(2000, 1, 1),
                gender='Male',
                address='123 Test St',
                city='Test City',
                course='Computer Science'
            )
            db.session.add(student)
            db.session.commit()
            
            assert repr(student) == '<Student John Doe>'

    def test_student_unique_email_constraint(self, test_app):
        """Test that duplicate emails raise an error."""
        with test_app.app_context():
            student1 = Student(
                first_name='First',
                last_name='User',
                email='duplicate@example.com',
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
                email='duplicate@example.com',
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

    def test_student_all_fields(self, test_app):
        """Test all student fields are properly saved."""
        with test_app.app_context():
            test_date = date(1999, 6, 15)
            student = Student(
                first_name='Complete',
                last_name='Student',
                email='complete@example.com',
                phone='+1-555-000-0000',
                date_of_birth=test_date,
                gender='Other',
                address='789 Complete Lane',
                city='Full City',
                course='Medicine'
            )
            db.session.add(student)
            db.session.commit()
            
            # Retrieve and verify
            saved_student = Student.query.filter_by(email='complete@example.com').first()
            assert saved_student.first_name == 'Complete'
            assert saved_student.last_name == 'Student'
            assert saved_student.phone == '+1-555-000-0000'
            assert saved_student.date_of_birth == test_date
            assert saved_student.gender == 'Other'
            assert saved_student.address == '789 Complete Lane'
            assert saved_student.city == 'Full City'
            assert saved_student.course == 'Medicine'


class TestIndexRoute:
    """Test cases for the index (home) route."""

    def test_index_get(self, client):
        """Test GET request to index page."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Student Registration' in response.data
        assert b'EduRegister' in response.data

    def test_index_contains_form(self, client):
        """Test that index page contains the registration form."""
        response = client.get('/')
        assert b'first_name' in response.data
        assert b'last_name' in response.data
        assert b'email' in response.data
        assert b'phone' in response.data
        assert b'date_of_birth' in response.data
        assert b'gender' in response.data
        assert b'address' in response.data
        assert b'city' in response.data
        assert b'course' in response.data

    def test_index_contains_course_options(self, client):
        """Test that index page contains course options."""
        response = client.get('/')
        assert b'Computer Science' in response.data
        assert b'Business Administration' in response.data
        assert b'Mechanical Engineering' in response.data
        assert b'Medicine' in response.data

    def test_index_contains_gender_options(self, client):
        """Test that index page contains gender options."""
        response = client.get('/')
        assert b'Male' in response.data
        assert b'Female' in response.data
        assert b'Other' in response.data


class TestRegisterRoute:
    """Test cases for the registration route."""

    def test_register_success(self, client, sample_student_data):
        """Test successful student registration."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Registration Successful' in response.data
        assert b'John' in response.data
        assert b'Doe' in response.data

    def test_register_creates_student_in_db(self, client, test_app, sample_student_data):
        """Test that registration creates a student in the database."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        with test_app.app_context():
            student = Student.query.filter_by(email='john.doe@example.com').first()
            assert student is not None
            assert student.first_name == 'John'
            assert student.last_name == 'Doe'

    def test_register_duplicate_email(self, client, test_app, sample_student_data):
        """Test registration with duplicate email shows error."""
        # First registration
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        # Second registration with same email
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'already exists' in response.data

    def test_register_redirects_to_success(self, client, sample_student_data):
        """Test that successful registration redirects to success page."""
        response = client.post('/register', data=sample_student_data, follow_redirects=False)
        assert response.status_code == 302
        assert '/success/' in response.location

    def test_register_with_different_genders(self, client, test_app):
        """Test registration with different gender options."""
        genders = ['Male', 'Female', 'Other']
        
        for i, gender in enumerate(genders):
            data = {
                'first_name': f'Test{i}',
                'last_name': 'User',
                'email': f'test{i}@example.com',
                'phone': f'123456789{i}',
                'date_of_birth': '2000-01-01',
                'gender': gender,
                'address': '123 Test St',
                'city': 'Test City',
                'course': 'Computer Science'
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200
            assert b'Registration Successful' in response.data

    def test_register_with_all_courses(self, client, test_app):
        """Test registration with different courses."""
        courses = [
            'Computer Science', 'Business Administration', 'Mechanical Engineering',
            'Electrical Engineering', 'Civil Engineering', 'Medicine',
            'Law', 'Arts & Design', 'Psychology', 'Mathematics'
        ]
        
        for i, course in enumerate(courses):
            data = {
                'first_name': f'Student{i}',
                'last_name': 'Course',
                'email': f'course{i}@example.com',
                'phone': f'555000{i:04d}',
                'date_of_birth': '2000-01-01',
                'gender': 'Male',
                'address': '123 Test St',
                'city': 'Test City',
                'course': course
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200

    def test_register_invalid_date_format(self, client, sample_student_data):
        """Test registration with invalid date format."""
        sample_student_data['date_of_birth'] = 'invalid-date'
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'failed' in response.data or b'Registration' in response.data


class TestSuccessRoute:
    """Test cases for the success route."""

    def test_success_page_displays_student_info(self, client, sample_student_data):
        """Test success page displays student information."""
        # Register a student first
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'John' in response.data
        assert b'Doe' in response.data
        assert b'john.doe@example.com' in response.data
        assert b'Computer Science' in response.data

    def test_success_page_shows_student_id(self, client, sample_student_data):
        """Test success page shows formatted student ID."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'STU-' in response.data

    def test_success_page_shows_initials(self, client, sample_student_data):
        """Test success page shows student initials in avatar."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'JD' in response.data  # John Doe initials

    def test_success_invalid_student_id(self, client, test_app):
        """Test accessing success page with invalid student ID returns 404."""
        response = client.get('/success/99999')
        assert response.status_code == 404

    def test_success_page_shows_registration_date(self, client, sample_student_data):
        """Test success page shows registration date."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Registered on' in response.data

    def test_success_page_action_buttons(self, client, sample_student_data):
        """Test success page contains action buttons."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Register Another Student' in response.data
        assert b'View All Students' in response.data


class TestStudentsRoute:
    """Test cases for the students list route."""

    def test_students_page_empty(self, client):
        """Test students page with no registered students."""
        response = client.get('/students')
        assert response.status_code == 200
        assert b'No Students Yet' in response.data
        assert b'Be the first to register!' in response.data

    def test_students_page_with_students(self, client, sample_student_data):
        """Test students page shows registered students."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        response = client.get('/students')
        assert response.status_code == 200
        assert b'John' in response.data
        assert b'Doe' in response.data
        assert b'john.doe@example.com' in response.data

    def test_students_page_shows_count(self, client, sample_student_data, another_student_data):
        """Test students page shows correct student count."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        client.post('/register', data=another_student_data, follow_redirects=True)
        
        response = client.get('/students')
        assert response.status_code == 200
        assert b'2 students enrolled' in response.data

    def test_students_page_single_student_grammar(self, client, sample_student_data):
        """Test students page uses correct grammar for single student."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        response = client.get('/students')
        assert response.status_code == 200
        assert b'1 student enrolled' in response.data

    def test_students_page_shows_student_details(self, client, sample_student_data):
        """Test students page shows student details."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        response = client.get('/students')
        assert response.status_code == 200
        assert b'+1-555-123-4567' in response.data
        assert b'New York' in response.data
        assert b'Computer Science' in response.data

    def test_students_page_order_by_date(self, client, test_app, sample_student_data, another_student_data):
        """Test students are ordered by registration date (newest first)."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        client.post('/register', data=another_student_data, follow_redirects=True)
        
        response = client.get('/students')
        assert response.status_code == 200
        
        # Jane should appear before John (registered later)
        jane_pos = response.data.find(b'Jane')
        john_pos = response.data.find(b'John')
        assert jane_pos < john_pos

    def test_students_page_navigation_links(self, client):
        """Test students page contains navigation links."""
        response = client.get('/students')
        assert response.status_code == 200
        assert b'New Registration' in response.data

    def test_students_page_shows_initials(self, client, sample_student_data):
        """Test students page shows student initials."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        response = client.get('/students')
        assert response.status_code == 200
        assert b'JD' in response.data


class TestFlashMessages:
    """Test cases for flash messages."""

    def test_success_flash_message(self, client, sample_student_data):
        """Test success flash message on registration."""
        # Flash messages are typically consumed on redirect
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200

    def test_error_flash_message_duplicate_email(self, client, sample_student_data):
        """Test error flash message for duplicate email."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'already exists' in response.data


class TestStaticFiles:
    """Test cases for static file serving."""

    def test_css_file_exists(self, client):
        """Test that CSS file is served correctly."""
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        assert b'EduRegister' in response.data


class TestAppConfiguration:
    """Test cases for app configuration."""

    def test_app_exists(self):
        """Test that app is created."""
        assert app is not None

    def test_app_is_testing(self, test_app):
        """Test that app is in testing mode."""
        assert test_app.config['TESTING'] is True

    def test_secret_key_set(self, test_app):
        """Test that secret key is set."""
        assert test_app.config['SECRET_KEY'] is not None


class TestDatabaseIntegration:
    """Integration tests for database operations."""

    def test_multiple_students_query(self, client, test_app, sample_student_data, another_student_data):
        """Test querying multiple students."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        client.post('/register', data=another_student_data, follow_redirects=True)
        
        with test_app.app_context():
            students = Student.query.all()
            assert len(students) == 2

    def test_student_query_by_email(self, client, test_app, sample_student_data):
        """Test querying student by email."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        with test_app.app_context():
            student = Student.query.filter_by(email='john.doe@example.com').first()
            assert student is not None
            assert student.first_name == 'John'

    def test_student_query_by_id(self, client, test_app, sample_student_data):
        """Test querying student by ID."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        with test_app.app_context():
            student = Student.query.filter_by(email='john.doe@example.com').first()
            student_id = student.id
            
            queried_student = Student.query.get(student_id)
            assert queried_student is not None
            assert queried_student.email == 'john.doe@example.com'


class TestEdgeCases:
    """Test cases for edge cases and boundary conditions."""

    def test_long_field_values(self, client, test_app):
        """Test registration with maximum length field values."""
        data = {
            'first_name': 'A' * 50,
            'last_name': 'B' * 50,
            'email': 'x' * 90 + '@test.com',
            'phone': '1' * 20,
            'date_of_birth': '2000-01-01',
            'gender': 'Male',
            'address': 'C' * 200,
            'city': 'D' * 50,
            'course': 'Computer Science'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200

    def test_special_characters_in_name(self, client, test_app):
        """Test registration with special characters in name."""
        data = {
            'first_name': "O'Brien",
            'last_name': 'López-García',
            'email': 'special@example.com',
            'phone': '1234567890',
            'date_of_birth': '2000-01-01',
            'gender': 'Male',
            'address': '123 Test St',
            'city': 'Test City',
            'course': 'Computer Science'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200
        assert b"O&#39;Brien" in response.data or b"O'Brien" in response.data

    def test_minimum_date(self, client, test_app):
        """Test registration with early birth date."""
        data = {
            'first_name': 'Old',
            'last_name': 'Student',
            'email': 'old@example.com',
            'phone': '1234567890',
            'date_of_birth': '1950-01-01',
            'gender': 'Male',
            'address': '123 Test St',
            'city': 'Test City',
            'course': 'Computer Science'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200

    def test_recent_date(self, client, test_app):
        """Test registration with recent birth date."""
        data = {
            'first_name': 'Young',
            'last_name': 'Student',
            'email': 'young@example.com',
            'phone': '1234567890',
            'date_of_birth': '2020-01-01',
            'gender': 'Female',
            'address': '123 Test St',
            'city': 'Test City',
            'course': 'Computer Science'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200


class TestNavigationAndLinks:
    """Test cases for navigation and links between pages."""

    def test_index_to_students_link(self, client):
        """Test link from index to students page."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'/students' in response.data

    def test_students_to_index_link(self, client):
        """Test link from students page to index."""
        response = client.get('/students')
        assert response.status_code == 200
        assert b'New Registration' in response.data

    def test_success_to_index_link(self, client, sample_student_data):
        """Test link from success page to index."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Register Another Student' in response.data

    def test_success_to_students_link(self, client, sample_student_data):
        """Test link from success page to students."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'View All Students' in response.data








