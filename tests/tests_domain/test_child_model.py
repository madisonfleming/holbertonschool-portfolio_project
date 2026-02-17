import unittest
from unittest.mock import patch
from app.domain.child import Child
from datetime import date
from app.domain.exceptions import InvalidChildNameError


class TestChild(unittest.TestCase):
    def setUp(self):
        """
        constructs valid child data that can be used in tests
        """
        self.happy_child = {
            'name' : 'Adam',
            'date_of_birth' : date(2023, 12, 5), # Year, Month, Day
            'avatar_url' : None
            }

    @patch('app.domain.base.uuid.uuid4')
    def test_create_valid_child(self, mock_uuid):
        """
        Happy path: tests the constructor, setters and to_dict method with valid data
        """ 
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        child = Child(**self.happy_child)
        expected_data = {
            'name' : 'Adam',
            'child_id' : '123e4567-e89b-12d3-a456-426614174000',
            'date_of_birth' : '2023-12-05',
            'age' : child.age, # note: valid age is tested separately
            'avatar_url' : None
        }
        self.assertDictEqual(child.to_dict(), expected_data) # validate instance becomes dict per to_dict by asserting both dicts are same

    @patch('app.domain.base.uuid.uuid4')
    def test_empty_name(self, mock_uuid):
        """
        Negative path: tests the name validation in setter logic (raises ValueError if name is empty)
        """
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        with self.assertRaises(InvalidChildNameError): # error message not included in case of message change
            Child(name="", date_of_birth=date(2023, 12, 5))

    @patch('app.domain.base.uuid.uuid4')
    def test_name_data_type(self, mock_uuid):
        """
        Negative path: tests the name validation in setter logic (raises ValueError if name is not string)
        """
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        with self.assertRaises(TypeError): # error message not included in case of message change
            Child(name=111, date_of_birth=date(2023, 12, 5))

    @patch('app.domain.base.uuid.uuid4')
    def test_dob_data_type(self, mock_uuid):
        """
        Negative path: tests the DOB validation in setter logic (raises TypeError if DOB is not a date)
        """
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        with self.assertRaises(TypeError): # error message not included in case of message change
            Child(name="Adam", date_of_birth="2023-12-05")

    @patch('app.domain.base.uuid.uuid4')
    def test_valid_age1(self, mock_uuid):
        """
        Happy path: tests the age logic is correct when birthday in current year hasn't occured yet
        """
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        # note: unable to patch date.today (immutable), test will fail on 5/12/26 on the assertion child is age 2
        child = Child(name='Adam', date_of_birth=date(2023, 12, 5))
        self.assertEqual(child.age, 2)

    @patch('app.domain.base.uuid.uuid4')
    def test_valid_age2(self, mock_uuid):
        """
        Happy path: tests the age logic is correct when birthday in current year has already occured
        """
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        # note: unable to patch date.today (immutable), test will fail on 13/2/27 on the assertion child is age 3
        child = Child(name='Adam', date_of_birth=date(2023, 2, 13))
        self.assertEqual(child.age, 3)

    def test_child_model_instance_attributes(self):
        """ 
        Happy path: tests that the child_model instance attributes haven't been inadvertently changed
        """
        child = Child(**self.happy_child)
        expected_keys = ['id', 'created_at', 'updated_at', '_name', '_date_of_birth', 'avatar_url']
        child_keys = list(child.__dict__.keys())
        self.assertEqual(child_keys, expected_keys)


if __name__ == "__main__":
    unittest.main()
