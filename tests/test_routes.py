"""
Unit tests specifically for Flask routes.
"""
import pytest
from datetime import datetime, date
from app import db, Student


class TestIndexRouteResponses:
    """Test HTTP responses for index route."""

    def test_index_method_get_allowed(self, client):
        """Test GET method is allowed on index."""
        response = client.get('/')
        assert response.status_code == 200

    def test_index_content_type(self, client):
        """Test content type of index response."""
        response = client.get('/')
        assert 'text/html' in response.content_type


class TestRegisterRouteResponses:
    """Test HTTP responses for register route."""

    def test_register_method_post_allowed(self, client, sample_student_data):
        """Test POST method is allowed on register."""
        response = client.post('/register', data=sample_student_data)
        assert response.status_code in [200, 302]

    def test_register_method_get_not_allowed(self, client):
        """Test GET method returns 405 on register."""
        response = client.get('/register')
        assert response.status_code == 405

    def test_register_empty_form(self, client):
        """Test submitting empty form."""
        response = client.post('/register', data={})
        # Should either redirect or show error
        assert response.status_code in [200, 302, 400, 500]

    def test_register_partial_data(self, client):
        """Test submitting partial data."""
        data = {
            'first_name': 'Partial',
            'last_name': 'Data'
        }
        response = client.post('/register', data=data)
        assert response.status_code in [200, 302, 400, 500]


class TestSuccessRouteResponses:
    """Test HTTP responses for success route."""

    def test_success_method_get_allowed(self, client, sample_student_data):
        """Test GET method is allowed on success with valid ID."""
        # First create a student
        client.post('/register', data=sample_student_data)
        response = client.get('/success/1')
        assert response.status_code == 200

    def test_success_method_post_not_allowed(self, client, sample_student_data):
        """Test POST method returns 405 on success."""
        client.post('/register', data=sample_student_data)
        response = client.post('/success/1', data={})
        assert response.status_code == 405

    def test_success_nonexistent_id(self, client):
        """Test accessing success page with non-existent ID."""
        response = client.get('/success/99999')
        assert response.status_code == 404

    def test_success_invalid_id_format(self, client):
        """Test accessing success page with invalid ID format."""
        response = client.get('/success/invalid')
        assert response.status_code == 404


class TestStudentsRouteResponses:
    """Test HTTP responses for students route."""

    def test_students_method_get_allowed(self, client):
        """Test GET method is allowed on students."""
        response = client.get('/students')
        assert response.status_code == 200

    def test_students_content_type(self, client):
        """Test content type of students response."""
        response = client.get('/students')
        assert 'text/html' in response.content_type


class TestEditStudentRouteResponses:
    """Test HTTP responses for edit student route."""

    def test_edit_get_allowed(self, client, sample_student_data, test_app):
        client.post('/register', data=sample_student_data, follow_redirects=True)
        with test_app.app_context():
            student = Student.query.filter_by(email='john.doe@example.com').first()
            student_id = student.id
        response = client.get(f'/students/{student_id}/edit')
        assert response.status_code == 200

    def test_edit_post_updates(self, client, sample_student_data, test_app):
        client.post('/register', data=sample_student_data, follow_redirects=True)
        with test_app.app_context():
            student = Student.query.filter_by(email='john.doe@example.com').first()
            student_id = student.id
        updated = sample_student_data.copy()
        updated['city'] = 'Chicago'
        response = client.post(f'/students/{student_id}/edit', data=updated, follow_redirects=True)
        assert response.status_code in [200, 302]

    def test_edit_nonexistent_returns_404(self, client):
        response = client.get('/students/99999/edit')
        assert response.status_code == 404

    def test_edit_duplicate_email_blocked(self, client, sample_student_data, another_student_data, test_app):
        client.post('/register', data=sample_student_data, follow_redirects=True)
        client.post('/register', data=another_student_data, follow_redirects=True)
        with test_app.app_context():
            target = Student.query.filter_by(email='john.doe@example.com').first()
            target_id = target.id
        updated = sample_student_data.copy()
        updated['email'] = another_student_data['email']
        response = client.post(f'/students/{target_id}/edit', data=updated, follow_redirects=True)
        assert response.status_code == 200
        assert b'already exists' in response.data


class TestDeleteStudentRouteResponses:
    """Test HTTP responses for delete student route."""

    def test_delete_method_post_allowed(self, client, sample_student_data, test_app):
        """Test POST method deletes a student."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        with test_app.app_context():
            student = Student.query.filter_by(email='john.doe@example.com').first()
            student_id = student.id

        response = client.post(f'/students/{student_id}/delete', follow_redirects=False)
        assert response.status_code in [302, 200]

    def test_delete_method_get_not_allowed(self, client, sample_student_data, test_app):
        """Test GET method returns 405 on delete route."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        with test_app.app_context():
            student = Student.query.filter_by(email='john.doe@example.com').first()
            student_id = student.id

        response = client.get(f'/students/{student_id}/delete')
        assert response.status_code == 405

    def test_delete_nonexistent_returns_404(self, client):
        """Test deleting non-existent student returns 404."""
        response = client.post('/students/99999/delete')
        assert response.status_code == 404


class TestStaticRoutes:
    """Test static file serving."""

    def test_static_css_served(self, client):
        """Test CSS file is served."""
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        assert 'text/css' in response.content_type

    def test_static_nonexistent_returns_404(self, client):
        """Test non-existent static file returns 404."""
        response = client.get('/static/css/nonexistent.css')
        assert response.status_code == 404


class TestRouteIntegration:
    """Integration tests for route workflows."""

    def test_complete_registration_flow(self, client, sample_student_data):
        """Test complete registration workflow."""
        # Step 1: Access index
        response = client.get('/')
        assert response.status_code == 200
        
        # Step 2: Submit registration
        response = client.post('/register', data=sample_student_data, follow_redirects=False)
        assert response.status_code == 302
        
        # Step 3: Follow redirect to success
        response = client.get(response.location)
        assert response.status_code == 200
        assert b'Registration Successful' in response.data
        
        # Step 4: View all students
        response = client.get('/students')
        assert response.status_code == 200
        assert b'John' in response.data

    def test_multiple_registrations_flow(self, client, sample_student_data, another_student_data):
        """Test multiple registrations workflow."""
        # Register first student
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        # Register second student
        client.post('/register', data=another_student_data, follow_redirects=True)
        
        # Verify both in list
        response = client.get('/students')
        assert b'John' in response.data
        assert b'Jane' in response.data
        assert b'2 students enrolled' in response.data

    def test_duplicate_prevention_flow(self, client, sample_student_data):
        """Test duplicate email prevention workflow."""
        # First registration
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'Registration Successful' in response.data
        
        # Attempt duplicate
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'already exists' in response.data
        
        # Verify only one in database
        response = client.get('/students')
        assert b'1 student enrolled' in response.data


class TestRouteContentValidation:
    """Test route content validation."""

    def test_index_has_form_action(self, client):
        """Test index form has correct action."""
        response = client.get('/')
        assert b'action="/register"' in response.data

    def test_index_has_method_post(self, client):
        """Test index form uses POST method."""
        response = client.get('/')
        assert b'method="POST"' in response.data

    def test_index_has_required_inputs(self, client):
        """Test index has all required input fields."""
        response = client.get('/')
        required_fields = [
            b'name="first_name"',
            b'name="last_name"',
            b'name="email"',
            b'name="phone"',
            b'name="date_of_birth"',
            b'name="gender"',
            b'name="address"',
            b'name="city"',
            b'name="course"'
        ]
        for field in required_fields:
            assert field in response.data

    def test_success_has_student_info(self, client, sample_student_data):
        """Test success page displays student info."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        
        # Check for expected content
        assert b'John' in response.data
        assert b'Doe' in response.data
        assert b'john.doe@example.com' in response.data

    def test_students_has_proper_structure(self, client, sample_student_data):
        """Test students page has proper structure."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        
        response = client.get('/students')
        assert b'Registered Students' in response.data
        assert b'enrolled' in response.data


class TestErrorHandling:
    """Test error handling in routes."""

    def test_404_for_unknown_route(self, client):
        """Test 404 for unknown routes."""
        response = client.get('/unknown-route')
        assert response.status_code == 404

    def test_register_handles_exception(self, client):
        """Test register handles exceptions gracefully."""
        # Submit with invalid date that can't be parsed
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'phone': '1234567890',
            'date_of_birth': 'not-a-date',
            'gender': 'Male',
            'address': '123 Test St',
            'city': 'Test City',
            'course': 'Computer Science'
        }
        response = client.post('/register', data=data, follow_redirects=True)
        # Should not crash, redirect with error message
        assert response.status_code == 200








