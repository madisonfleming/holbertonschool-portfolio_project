import unittest
from unittest.mock import patch
from app.domain.milestone import Milestone
from app.domain.exceptions import InvalidMilestoneNameError, InvalidMilestoneThresholdError

class TestMilestone(unittest.TestCase):
    def setUp(self):
        self.milestone_data = {
            "name": "100 Books",
            "description": "You've read 100 books! Superstar!",
            "metric_key": "books_read",
            "threshold": 100
        }

    def test_milestone_model_instance_attributes(self):
        """ Checks that the milestone_model instance atrributes
          haven't changed. Protects against drift between milestone_model and 
          unit test implementation. """


        milestone = Milestone(**self.milestone_data)
        expected_keys = ['id', 'created_at', 'updated_at', '_name', '_description', '_metric_key', '_threshold']
        milestone_keys = list(milestone.__dict__.keys())
        print(milestone_keys)
        self.assertEqual(milestone_keys, expected_keys)

    @patch('app.domain.base.uuid.uuid4')
    def test_create_a_milestone_and_return_dict(self, mock_uuid):
        mock_uuid.return_value = '123e4567-e89b-12d3-a456-426614174000'
        milestone = Milestone(**self.milestone_data)
        expected_data = {
            "ms_type_id": mock_uuid.return_value,
            "name": self.milestone_data['name'],
            "description": self.milestone_data['description'],
            "metric_key": self.milestone_data['metric_key'],
            "threshold": self.milestone_data['threshold'],
        }

        self.assertEqual(milestone.to_dict(), expected_data)

    def test_name_validations_when_name_is_empty(self):
        self.milestone_data['name'] = None
        with self.assertRaises(InvalidMilestoneNameError):
            Milestone(**self.milestone_data)
    
    def test_name_validations_when_name_is_not_string(self):
        self.milestone_data['name'] = 123
        with self.assertRaises(InvalidMilestoneNameError):
            Milestone(**self.milestone_data)

    def test_threshold_validations_when_threshold_is_empty(self):
        self.milestone_data['threshold'] = None
        with self.assertRaises(InvalidMilestoneThresholdError):
            Milestone(**self.milestone_data)
    
    def test_threshold_validations_when_threshold_is_not_int(self):
        self.milestone_data['threshold'] = ['123', 123]
        with self.assertRaises(ValueError):
            Milestone(**self.milestone_data)

    def test_threshold_validations_when_threshold_below_one(self):
        self.milestone_data['threshold'] = -4
        with self.assertRaises(InvalidMilestoneThresholdError):
            Milestone(**self.milestone_data)