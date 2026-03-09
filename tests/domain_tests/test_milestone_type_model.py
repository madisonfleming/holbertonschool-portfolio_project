import unittest
from datetime import datetime, timezone
from unittest.mock import patch
from app.domain.milestone_type import MilestoneType
from app.domain.exceptions import InvalidMilestoneNameError, InvalidMilestoneThresholdError

class TestMilestone(unittest.TestCase):
    def setUp(self):
        self.milestone_data = {
            "name": "100 Books",
            "subject": "Elephants",
            "type": "books_read",
            "threshold": 100,
        }

    def test_milestone_model_instance_attributes(self):
        """ Checks that the milestone_model instance atrributes
          haven't changed. Protects against drift between milestone_model and 
          unit test implementation. """


        milestone = MilestoneType(**self.milestone_data)
        expected_keys = ["id", "created_at", "updated_at", "_name", "_subject", "_type", "_threshold"]
        milestone_keys = list(milestone.__dict__.keys())
        self.assertEqual(milestone_keys, expected_keys)

    @patch("app.domain.base.uuid.uuid4")
    @patch("app.domain.base.datetime")
    def test_create_a_milestone_and_return_dict(self, mock_timestamp, mock_uuid):
        mock_uuid.return_value = "123e4567-e89b-12d3-a456-426614174000"
        fixed_timestamp = datetime(2026, 2, 21, 23, 59, 56, 518662, tzinfo=timezone.utc)
        mock_timestamp.now.return_value = fixed_timestamp
        
        milestone = MilestoneType(**self.milestone_data)
        expected_data = {
            "created_at": fixed_timestamp.isoformat(),
            "updated_at": fixed_timestamp.isoformat(),
            "id": mock_uuid.return_value,
            "name": self.milestone_data["name"],
            "subject": self.milestone_data["subject"],
            "type": self.milestone_data["type"],
            "threshold": self.milestone_data["threshold"],
        }

        self.assertEqual(milestone.to_dict(), expected_data)

    def test_name_validations_when_name_is_empty(self):
        self.milestone_data["name"] = None
        with self.assertRaises(InvalidMilestoneNameError):
            MilestoneType(**self.milestone_data)
    
    def test_name_validations_when_name_is_not_string(self):
        self.milestone_data["name"] = 123
        with self.assertRaises(InvalidMilestoneNameError):
            MilestoneType(**self.milestone_data)

    def test_threshold_validations_when_threshold_is_empty(self):
        self.milestone_data["threshold"] = None
        with self.assertRaises(InvalidMilestoneThresholdError):
            MilestoneType(**self.milestone_data)
    
    def test_threshold_validations_when_threshold_is_not_int(self):
        self.milestone_data["threshold"] = ["123", 123]
        with self.assertRaises(ValueError):
            MilestoneType(**self.milestone_data)

    def test_threshold_validations_when_threshold_below_one(self):
        self.milestone_data["threshold"] = -4
        with self.assertRaises(InvalidMilestoneThresholdError):
            MilestoneType(**self.milestone_data)