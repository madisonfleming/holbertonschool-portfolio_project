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

    def test_user_model_instance_attributes(self):
        """ Checks that the user_model instance atrributes
          haven't changed. Protects against drift between user_model and 
          unit test implementation. """
        
        user = User(**self.standard_data)
        expected_keys = ['id', 'created_at', 'updated_at', '_name', '_email', '_role', 'firebase_uid']
        user_keys = list(user.__dict__.keys())
        self.assertEqual(user_keys, expected_keys)

    @patch('app.domain.base.uuid.uuid4')
    def test_create_standard_user_with_no_role(self, mock_uuid):
        """ Create a standard user when a role argument is not provided """

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

    @patch('app.domain.base.uuid.uuid4')
    def test_create_admin_user_with_admin_role(self, mock_uuid):
        """ Create an admin user when role=admin argument is provided """

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

    @patch('app.domain.base.uuid.uuid4')
    def test_create_standard_user_with_standard_role(self, mock_uuid):
        """ Create a standard user when role=standard argument is provided """

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

    def test_name_validations_when_name_is_empty(self):
        self.standard_data['name'] = ''

        with self.assertRaises(ValueError):
            User(**self.standard_data)

    def test_name_validations_when_name_is_not_string(self):
        self.standard_data['name'] = 123.45

        with self.assertRaises(TypeError):
            User(**self.standard_data)
    
    def test_email_validations_when_email_is_empty(self):
        self.standard_data['email'] = ''

        with self.assertRaises(ValueError):
            User(**self.standard_data)

    def test_email_validations_when_email_is_not_string(self):
        self.standard_data['email'] = 123.45

        with self.assertRaises(TypeError):
            User(**self.standard_data)
    
    def test_role_validation_when_role_is_neither_standard_nor_admin(self):
        self.standard_data['role'] = 'adm1n'
        user = User(**self.standard_data)
        self.assertEqual(user.role, 'standard')
    
    def test_role_validation_when_role_is_not_string(self):
        self.standard_data['role'] = ['admin']
        with self.assertRaises(TypeError):
            User(**self.standard_data)

    def test_update_profile_with_valid_name_and_email_changes(self):
        user = User(**self.standard_data)
        timestamp_before_update = user.updated_at

        updated_data = {
            'name': 'Adam',
            'email': 'adam@example.com'
        }
        
        user.update_profile(updated_data)
        self.assertNotEqual(timestamp_before_update, user.updated_at)
        self.assertEqual(user.name, updated_data['name'])
        self.assertEqual(user.email, updated_data['email'])

    def test_update_profile_with_extra_fields_included(self):
        user = User(**self.standard_data)
        timestamp_before_update = user.updated_at

        updated_data = {
            'name': 'Adam',
            'email': 'adam@example.com',
            'extra_field': 'my new field'
        }
        
        user.update_profile(updated_data)
        self.assertNotEqual(timestamp_before_update, user.updated_at)
        self.assertEqual(user.name, updated_data['name'])
        self.assertEqual(user.email, updated_data['email'])

    def test_update_profile_with_only_extra_fields(self):
        user = User(**self.standard_data)
        timestamp_before_update = user.updated_at

        updated_data = {
            'extra_field': 'my new field'
        }
        
        user.update_profile(updated_data)
        self.assertNotEqual(timestamp_before_update, user.updated_at)
        self.assertEqual(user.name, self.standard_data['name'])
        self.assertEqual(user.email, self.standard_data['email'])

    def test_update_profile_does_not_affect_role(self):
        user = User(**self.standard_data)
        timestamp_before_update = user.updated_at

        updated_data = {
            'role': 'admin'
        }
        
        user.update_profile(updated_data)
        self.assertNotEqual(timestamp_before_update, user.updated_at)
        self.assertEqual(user.role, 'standard')

    def test_update_profile_validations_when_name_is_not_provided(self):
        user = User(**self.standard_data)
        timestamp_before_update = user.updated_at

        updated_data = {
            'name': ''
        }
        
        with self.assertRaises(ValueError):
            user.update_profile(updated_data)
        self.assertEqual(timestamp_before_update, user.updated_at)
        self.assertEqual(user.name, self.standard_data['name'])
        self.assertEqual(user.email, self.standard_data['email'])

    def test_update_profile_validations_when_name_is_not_string(self):
        user = User(**self.standard_data)
        timestamp_before_update = user.updated_at

        updated_data = {
            'name': 123
        }
        
        with self.assertRaises(TypeError):
            user.update_profile(updated_data)
        self.assertEqual(timestamp_before_update, user.updated_at)
        self.assertEqual(user.name, self.standard_data['name'])
        self.assertEqual(user.email, self.standard_data['email'])

    def test_update_profile_validations_when_email_is_not_provided(self):
        user = User(**self.standard_data)
        timestamp_before_update = user.updated_at

        updated_data = {
            'email': ''
        }
        
        with self.assertRaises(ValueError):
            user.update_profile(updated_data)
        self.assertEqual(timestamp_before_update, user.updated_at)
        self.assertEqual(user.name, self.standard_data['name'])
        self.assertEqual(user.email, self.standard_data['email'])

    def test_update_profile_validations_when_email_is_not_string(self):
        user = User(**self.standard_data)
        timestamp_before_update = user.updated_at

        updated_data = {
            'email': 123
        }
        
        with self.assertRaises(TypeError):
            user.update_profile(updated_data)
        self.assertEqual(timestamp_before_update, user.updated_at)
        self.assertEqual(user.name, self.standard_data['name'])
        self.assertEqual(user.email, self.standard_data['email'])



if __name__ == "__main__":
    unittest.main()
