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

    @patch('models.base.uuid.uuid4')
    def test_create_standard_user(self, mock_uuid):
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        standard_user = User(**self.standard_data)
        expected_data = {
            'id': '123e4567-e89b-12d3-a456-426614174000',
            'name': 'Marie',
            'email': 'marie@example.com',
            'role': 'standard'
        }
        self.assertDictEqual(standard_user.to_dict(), expected_data)


if __name__ == "__main__":
    unittest.main()
