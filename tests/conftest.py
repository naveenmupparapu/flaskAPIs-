"""
Pytest configuration and fixtures for the Student Registration Application.
"""
import pytest
import os
import sys
from datetime import datetime, date

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, Student


@pytest.fixture(scope='function')
def test_app():
    """Create and configure a new app instance for each test."""
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test-secret-key'
    
    # Create tables
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(test_app):
    """A test client for the app."""
    return test_app.test_client()


@pytest.fixture(scope='function')
def runner(test_app):
    """A test runner for the app's Click commands."""
    return test_app.test_cli_runner()


@pytest.fixture(scope='function')
def sample_student_data():
    """Sample student data for testing."""
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '+1-555-123-4567',
        'date_of_birth': '2000-05-15',
        'gender': 'Male',
        'address': '123 Main Street, Apt 4B',
        'city': 'New York',
        'course': 'Computer Science'
    }


@pytest.fixture(scope='function')
def another_student_data():
    """Another sample student data for testing."""
    return {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@example.com',
        'phone': '+1-555-987-6543',
        'date_of_birth': '1999-08-20',
        'gender': 'Female',
        'address': '456 Oak Avenue',
        'city': 'Los Angeles',
        'course': 'Business Administration'
    }


@pytest.fixture(scope='function')
def created_student(test_app, sample_student_data):
    """Create a student in the database."""
    with test_app.app_context():
        student = Student(
            first_name=sample_student_data['first_name'],
            last_name=sample_student_data['last_name'],
            email=sample_student_data['email'],
            phone=sample_student_data['phone'],
            date_of_birth=datetime.strptime(sample_student_data['date_of_birth'], '%Y-%m-%d').date(),
            gender=sample_student_data['gender'],
            address=sample_student_data['address'],
            city=sample_student_data['city'],
            course=sample_student_data['course']
        )
        db.session.add(student)
        db.session.commit()
        student_id = student.id
        return student_id








