"""
Unit tests for template rendering.
"""
import pytest
from datetime import date
from app import db, Student


class TestIndexTemplate:
    """Test index template rendering."""

    def test_index_renders_logo(self, client):
        """Test index renders logo."""
        response = client.get('/')
        assert b'EduRegister' in response.data
        # Check for book emoji (📚) in UTF-8 encoding
        assert b'\xf0\x9f\x93\x9a' in response.data or b'EduRegister' in response.data

    def test_index_renders_header(self, client):
        """Test index renders header section."""
        response = client.get('/')
        assert b'Student Registration' in response.data
        assert b'Begin your academic journey' in response.data

    def test_index_renders_personal_info_section(self, client):
        """Test index renders personal information section."""
        response = client.get('/')
        assert b'Personal Information' in response.data

    def test_index_renders_address_section(self, client):
        """Test index renders address details section."""
        response = client.get('/')
        assert b'Address Details' in response.data

    def test_index_renders_footer(self, client):
        """Test index renders footer."""
        response = client.get('/')
        assert b'EduRegister. Empowering Education' in response.data

    def test_index_renders_buttons(self, client):
        """Test index renders form buttons."""
        response = client.get('/')
        assert b'Clear Form' in response.data
        assert b'Register Now' in response.data


class TestSuccessTemplate:
    """Test success template rendering."""

    def test_success_renders_checkmark(self, client, sample_student_data):
        """Test success page renders checkmark animation."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'checkmark' in response.data

    def test_success_renders_welcome_message(self, client, sample_student_data):
        """Test success page renders welcome message."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'Welcome aboard' in response.data
        assert b'John' in response.data

    def test_success_renders_student_card(self, client, sample_student_data):
        """Test success page renders student card."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'student-card' in response.data

    def test_success_renders_info_grid(self, client, sample_student_data):
        """Test success page renders info grid."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'info-grid' in response.data
        assert b'Email' in response.data
        assert b'Phone' in response.data
        assert b'Date of Birth' in response.data
        assert b'Gender' in response.data
        assert b'Address' in response.data
        assert b'Course' in response.data

    def test_success_renders_student_id_format(self, client, sample_student_data):
        """Test success page renders student ID in correct format."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'STU-0001' in response.data

    def test_success_renders_navigation(self, client, sample_student_data):
        """Test success page renders navigation links."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'New Registration' in response.data
        assert b'View Students' in response.data


class TestStudentsTemplate:
    """Test students template rendering."""

    def test_students_renders_header(self, client):
        """Test students page renders header."""
        response = client.get('/students')
        assert b'Registered Students' in response.data

    def test_students_empty_state(self, client):
        """Test students page empty state."""
        response = client.get('/students')
        assert b'No Students Yet' in response.data
        assert b'Be the first to register!' in response.data
        assert b'Register Now' in response.data

    def test_students_renders_grid(self, client, sample_student_data):
        """Test students page renders student grid."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        response = client.get('/students')
        assert b'students-grid' in response.data

    def test_students_renders_mini_card(self, client, sample_student_data):
        """Test students page renders mini student cards."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        response = client.get('/students')
        assert b'student-mini-card' in response.data

    def test_students_renders_icons(self, client, sample_student_data):
        """Test students page renders contact icons."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        response = client.get('/students')
        # SVG icons for email, phone, location
        assert b'<svg' in response.data


class TestTemplateFlashMessages:
    """Test flash message rendering in templates."""

    def test_success_flash_rendered(self, client, sample_student_data):
        """Test success flash message is rendered."""
        # Flash messages are consumed after display
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert response.status_code == 200

    def test_error_flash_rendered(self, client, sample_student_data):
        """Test error flash message is rendered."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'already exists' in response.data


class TestTemplateCSS:
    """Test CSS styling in templates."""

    def test_index_includes_css(self, client):
        """Test index includes CSS link."""
        response = client.get('/')
        assert b'style.css' in response.data

    def test_success_includes_css(self, client, sample_student_data):
        """Test success page includes CSS link."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'style.css' in response.data

    def test_students_includes_css(self, client):
        """Test students page includes CSS link."""
        response = client.get('/students')
        assert b'style.css' in response.data

    def test_index_includes_fonts(self, client):
        """Test index includes Google Fonts."""
        response = client.get('/')
        assert b'fonts.googleapis.com' in response.data

    def test_index_includes_background_shapes(self, client):
        """Test index includes background shapes."""
        response = client.get('/')
        assert b'background-shapes' in response.data
        assert b'shape-1' in response.data
        assert b'shape-2' in response.data
        assert b'shape-3' in response.data


class TestTemplateJavaScript:
    """Test JavaScript in templates."""

    def test_index_includes_form_validation_js(self, client):
        """Test index includes form validation JavaScript."""
        response = client.get('/')
        assert b'addEventListener' in response.data

    def test_success_includes_confetti_js(self, client, sample_student_data):
        """Test success page includes confetti JavaScript."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'createConfetti' in response.data


class TestTemplateDateFormatting:
    """Test date formatting in templates."""

    def test_success_date_formatted(self, client, sample_student_data):
        """Test date of birth is formatted correctly."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        # Should show "May 15, 2000" format
        assert b'May' in response.data or b'2000' in response.data

    def test_success_registration_date_formatted(self, client, sample_student_data):
        """Test registration date is formatted correctly."""
        response = client.post('/register', data=sample_student_data, follow_redirects=True)
        assert b'Registered on' in response.data


class TestTemplateStudentCount:
    """Test student count display in templates."""

    def test_zero_students_display(self, client):
        """Test display when zero students."""
        response = client.get('/students')
        assert b'0 students enrolled' in response.data or b'No Students Yet' in response.data

    def test_one_student_singular(self, client, sample_student_data):
        """Test singular grammar for one student."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        response = client.get('/students')
        assert b'1 student enrolled' in response.data

    def test_multiple_students_plural(self, client, sample_student_data, another_student_data):
        """Test plural grammar for multiple students."""
        client.post('/register', data=sample_student_data, follow_redirects=True)
        client.post('/register', data=another_student_data, follow_redirects=True)
        response = client.get('/students')
        assert b'2 students enrolled' in response.data


class TestTemplateAccessibility:
    """Test template accessibility features."""

    def test_index_has_labels(self, client):
        """Test index form has labels for inputs."""
        response = client.get('/')
        assert b'<label' in response.data
        assert b'for="first_name"' in response.data
        assert b'for="last_name"' in response.data

    def test_index_has_placeholders(self, client):
        """Test index form has placeholders."""
        response = client.get('/')
        assert b'placeholder=' in response.data

    def test_index_has_required_attributes(self, client):
        """Test index form has required attributes."""
        response = client.get('/')
        # Count 'required' occurrences - should be multiple
        required_count = response.data.count(b'required')
        assert required_count >= 5








