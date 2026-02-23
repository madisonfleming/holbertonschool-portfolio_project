import unittest
from unittest.mock import patch
from app.domain.user import User
from app.domain.exceptions import InvalidEmailError, InvalidUserNameError
from datetime import datetime, timezone

class TestUser(unittest.TestCase):

    def setUp(self):
        """Constructs valid user data to be consumed by tests"""
        self.standard_data = {
            "name": "Marie",
            "email": "marie@example.com"
        }

        self.admin_data = {
            "name": "My Little Bookworm Admins",
            "email": "mlb@example.com",
            "role": "admin"
        }

    def test_user_model_instance_attributes(self):
        """ Checks that the user_model instance atrributes
          haven"t changed. Protects against drift between user_model and 
          unit test implementation. """
        
        user = User(**self.standard_data)
        expected_keys = ["id", "created_at", "updated_at", "_name", "_email", "_role", "firebase_uid"]
        user_keys = list(user.__dict__.keys())
        self.assertEqual(user_keys, expected_keys)

    @patch("app.domain.base.uuid.uuid4")
    @patch("app.domain.base.datetime")
    def test_create_standard_user_with_no_role(self, mock_timestamp, mock_uuid):
        """ Create a standard user when a role argument is not provided """

        mock_uuid.return_value = "123e4567-e89b-12d3-a456-426614174000"
        fixed_timestamp = datetime(2026, 2, 21, 23, 23, 56, 00, tzinfo=timezone.utc)
        mock_timestamp.now.return_value = fixed_timestamp

        standard_user = User(**self.standard_data)
        expected_data = {
            "created_at": fixed_timestamp.isoformat(),
            "updated_at": fixed_timestamp.isoformat(),
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": self.standard_data["name"],
            "email": self.standard_data["email"],
            "role": "standard",
            "firebase_uid": None
        }
        self.assertDictEqual(standard_user.to_dict(), expected_data)

    @patch("app.domain.base.uuid.uuid4")
    @patch("app.domain.base.datetime")
    def test_create_admin_user_with_admin_role(self, mock_timestamp, mock_uuid):
        """ Create an admin user when role=admin argument is provided """

        mock_uuid.return_value = "123e4567-e89b-12d3-a456-426614174000"
        fixed_timestamp = datetime(2026, 2, 21, 23, 23, 56, 00, tzinfo=timezone.utc)
        mock_timestamp.now.return_value = fixed_timestamp

        admin_user = User(**self.admin_data)
        expected_data = {
            "created_at": fixed_timestamp.isoformat(),
            "updated_at": fixed_timestamp.isoformat(),
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": self.admin_data["name"],
            "email": self.admin_data["email"],
            "role": "admin",
            "firebase_uid": None
        }
        self.assertDictEqual(admin_user.to_dict(), expected_data)

    @patch("app.domain.base.uuid.uuid4")
    @patch("app.domain.base.datetime")
    def test_create_standard_user_with_standard_role(self, mock_timestamp, mock_uuid):
        """ Create a standard user when role=standard argument is provided """

        mock_uuid.return_value = "123e4567-e89b-12d3-a456-426614174000"
        fixed_timestamp = datetime(2026, 2, 21, 23, 23, 56, 00, tzinfo=timezone.utc)
        mock_timestamp.now.return_value = fixed_timestamp

        self.standard_data["role"] = "standard"
        standard_user = User(**self.standard_data)
        expected_data = {
            "created_at": fixed_timestamp.isoformat(),
            "updated_at": fixed_timestamp.isoformat(),
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "name": self.standard_data["name"],
            "email": self.standard_data["email"],
            "role": "standard",
            "firebase_uid": None
        }
        self.assertDictEqual(standard_user.to_dict(), expected_data)

    def test_name_validations_when_name_is_empty(self):
        self.standard_data["name"] = ""

        with self.assertRaises(InvalidUserNameError):
            User(**self.standard_data)

    def test_name_validations_when_name_is_not_string(self):
        self.standard_data["name"] = 123.45

        with self.assertRaises(TypeError):
            User(**self.standard_data)
    
    def test_email_validations_when_email_is_empty(self):
        self.standard_data["email"] = ""

        with self.assertRaises(InvalidEmailError):
            User(**self.standard_data)

    def test_email_validations_when_email_is_not_string(self):
        self.standard_data["email"] = 123.45

        with self.assertRaises(TypeError):
            User(**self.standard_data)
    
    def test_role_validation_when_role_is_neither_standard_nor_admin(self):
        self.standard_data["role"] = "adm1n"
        user = User(**self.standard_data)
        self.assertEqual(user.role, "standard")
    
    def test_role_validation_when_role_is_not_string(self):
        self.standard_data["role"] = ["admin"]
        with self.assertRaises(TypeError):
            User(**self.standard_data)


if __name__ == "__main__":
    unittest.main()
