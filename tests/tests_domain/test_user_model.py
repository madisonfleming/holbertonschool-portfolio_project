import unittest
from unittest.mock import patch
from app.domain.user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        """Constructs valid user data to be consumed by tests"""
        self.standard_data = {
            'name': 'Marie',
            'email': 'marie@example.com'
        }

        self.admin_data = {
            'name': 'My Little Bookworm Admins',
            'email': 'mlb@example.com',
            'role': 'admin'
        }

    @patch('app.domain.base.uuid.uuid4')
    def test_create_standard_user_with_default_role(self, mock_uuid):
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        standard_user = User(**self.standard_data)
        expected_data = {
            'id': '123e4567-e89b-12d3-a456-426614174000',
            'name': self.standard_data['name'],
            'email': self.standard_data['email'],
            'role': 'standard',
            'firebase_uid': None
        }
        self.assertDictEqual(standard_user.to_dict(), expected_data)

    # Create admin user
    @patch('app.domain.base.uuid.uuid4')
    def test_create_admin_user(self, mock_uuid):
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        admin_user = User(**self.admin_data)
        expected_data = {
            'id': '123e4567-e89b-12d3-a456-426614174000',
            'name': self.admin_data['name'],
            'email': self.admin_data['email'],
            'role': 'admin',
            'firebase_uid': None
        }
        self.assertDictEqual(admin_user.to_dict(), expected_data)

    # Create standard user without role
    @patch('app.domain.base.uuid.uuid4')
    def test_create_standard_user_with_role(self, mock_uuid):
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        self.standard_data['role'] = 'standard'
        standard_user = User(**self.standard_data)
        expected_data = {
            'id': '123e4567-e89b-12d3-a456-426614174000',
            'name': self.standard_data['name'],
            'email': self.standard_data['email'],
            'role': 'standard',
            'firebase_uid': None
        }
        self.assertDictEqual(standard_user.to_dict(), expected_data)
# Test name validation
# Test email validation
# Test role validation
# Test update_profile(name, email)
# Test update_profile(name, email, role)
    



if __name__ == "__main__":
    unittest.main()
