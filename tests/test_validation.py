"""
Unit tests for data validation and edge cases.
"""
import pytest
from datetime import date
from app import db, Student


class TestEmailValidation:
    """Test email validation scenarios."""

    def test_valid_email_formats(self, client, test_app):
        """Test various valid email formats."""
        valid_emails = [
            'simple@example.com',
            'user.name@example.com',
            'user+tag@example.com',
            'user@subdomain.example.com',
            'user123@example.co.uk',
        ]
        
        for i, email in enumerate(valid_emails):
            data = {
                'first_name': f'User{i}',
                'last_name': 'Test',
                'email': email,
                'phone': f'123456789{i}',
                'date_of_birth': '2000-01-01',
                'gender': 'Male',
                'address': '123 Test St',
                'city': 'Test City',
                'course': 'Computer Science'
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200


class TestPhoneValidation:
    """Test phone number validation scenarios."""

    def test_various_phone_formats(self, client, test_app):
        """Test various phone number formats."""
        phones = [
            '1234567890',
            '+1-555-123-4567',
            '(555) 123-4567',
            '+44 20 7123 4567',
            '555.123.4567',
        ]
        
        for i, phone in enumerate(phones):
            data = {
                'first_name': f'Phone{i}',
                'last_name': 'Test',
                'email': f'phone{i}@example.com',
                'phone': phone,
                'date_of_birth': '2000-01-01',
                'gender': 'Male',
                'address': '123 Test St',
                'city': 'Test City',
                'course': 'Computer Science'
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200


class TestNameValidation:
    """Test name field validation scenarios."""

    def test_names_with_special_characters(self, client, test_app):
        """Test names with special characters."""
        names = [
            ("O'Brien", 'Smith'),
            ('Jean-Pierre', 'Dupont'),
            ('María', 'García'),
            ('José', 'González'),
            ('Müller', 'Schmidt'),
        ]
        
        for i, (first, last) in enumerate(names):
            data = {
                'first_name': first,
                'last_name': last,
                'email': f'name{i}@example.com',
                'phone': f'123456789{i}',
                'date_of_birth': '2000-01-01',
                'gender': 'Male',
                'address': '123 Test St',
                'city': 'Test City',
                'course': 'Computer Science'
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200

    def test_single_character_names(self, client, test_app):
        """Test single character names."""
        data = {
            'first_name': 'A',
            'last_name': 'B',
            'email': 'single@example.com',
            'phone': '1234567890',
            'date_of_birth': '2000-01-01',
            'gender': 'Male',
            'address': '123 Test St',
            'city': 'Test City',
            'course': 'Computer Science'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200


class TestDateValidation:
    """Test date validation scenarios."""

    def test_various_valid_dates(self, client, test_app):
        """Test various valid date formats."""
        dates = [
            '1990-01-01',
            '2000-12-31',
            '1985-06-15',
            '2010-02-28',
        ]
        
        for i, dob in enumerate(dates):
            data = {
                'first_name': f'Date{i}',
                'last_name': 'Test',
                'email': f'date{i}@example.com',
                'phone': f'123456789{i}',
                'date_of_birth': dob,
                'gender': 'Male',
                'address': '123 Test St',
                'city': 'Test City',
                'course': 'Computer Science'
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200


class TestAddressValidation:
    """Test address field validation scenarios."""

    def test_various_address_formats(self, client, test_app):
        """Test various address formats."""
        addresses = [
            '123 Main St',
            '456 Oak Avenue, Apt 4B',
            '789 First Street, Suite 100',
            '1 Infinite Loop',
            'P.O. Box 1234',
        ]
        
        for i, address in enumerate(addresses):
            data = {
                'first_name': f'Addr{i}',
                'last_name': 'Test',
                'email': f'addr{i}@example.com',
                'phone': f'123456789{i}',
                'date_of_birth': '2000-01-01',
                'gender': 'Male',
                'address': address,
                'city': 'Test City',
                'course': 'Computer Science'
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200


class TestCityValidation:
    """Test city field validation scenarios."""

    def test_various_city_names(self, client, test_app):
        """Test various city name formats."""
        cities = [
            'New York',
            'Los Angeles',
            'São Paulo',
            'München',
            "King's Landing",
        ]
        
        for i, city in enumerate(cities):
            data = {
                'first_name': f'City{i}',
                'last_name': 'Test',
                'email': f'city{i}@example.com',
                'phone': f'123456789{i}',
                'date_of_birth': '2000-01-01',
                'gender': 'Male',
                'address': '123 Test St',
                'city': city,
                'course': 'Computer Science'
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200


class TestCourseValidation:
    """Test course selection validation."""

    def test_all_available_courses(self, client, test_app):
        """Test all available course options."""
        courses = [
            'Computer Science',
            'Business Administration',
            'Mechanical Engineering',
            'Electrical Engineering',
            'Civil Engineering',
            'Medicine',
            'Law',
            'Arts & Design',
            'Psychology',
            'Mathematics'
        ]
        
        for i, course in enumerate(courses):
            data = {
                'first_name': f'Course{i}',
                'last_name': 'Test',
                'email': f'course_val{i}@example.com',
                'phone': f'123456789{i}',
                'date_of_birth': '2000-01-01',
                'gender': 'Male',
                'address': '123 Test St',
                'city': 'Test City',
                'course': course
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200


class TestGenderValidation:
    """Test gender selection validation."""

    def test_all_gender_options(self, client, test_app):
        """Test all gender options."""
        genders = ['Male', 'Female', 'Other']
        
        for i, gender in enumerate(genders):
            data = {
                'first_name': f'Gender{i}',
                'last_name': 'Test',
                'email': f'gender_val{i}@example.com',
                'phone': f'123456789{i}',
                'date_of_birth': '2000-01-01',
                'gender': gender,
                'address': '123 Test St',
                'city': 'Test City',
                'course': 'Computer Science'
            }
            response = client.post('/register', data=data, follow_redirects=True)
            assert response.status_code == 200


class TestBoundaryConditions:
    """Test boundary conditions and limits."""

    def test_max_length_first_name(self, client, test_app):
        """Test maximum length first name."""
        data = {
            'first_name': 'A' * 50,
            'last_name': 'Test',
            'email': 'maxfirst@example.com',
            'phone': '1234567890',
            'date_of_birth': '2000-01-01',
            'gender': 'Male',
            'address': '123 Test St',
            'city': 'Test City',
            'course': 'Computer Science'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200

    def test_max_length_address(self, client, test_app):
        """Test maximum length address."""
        data = {
            'first_name': 'Max',
            'last_name': 'Address',
            'email': 'maxaddr@example.com',
            'phone': '1234567890',
            'date_of_birth': '2000-01-01',
            'gender': 'Male',
            'address': 'A' * 200,
            'city': 'Test City',
            'course': 'Computer Science'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200

    def test_unicode_in_all_fields(self, client, test_app):
        """Test unicode characters in all fields."""
        data = {
            'first_name': 'Héléne',
            'last_name': 'Björk',
            'email': 'unicode@example.com',
            'phone': '+45 12 34 56 78',
            'date_of_birth': '2000-01-01',
            'gender': 'Female',
            'address': '123 Straße Weg',
            'city': 'München',
            'course': 'Arts & Design'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        assert response.status_code == 200








