import unittest
from datetime import datetime, timezone
from unittest.mock import patch
from app.domain.milestone_completion import MilestoneCompletion

class TestMilestoneCompletion(unittest.TestCase):
    def setUp(self):
        timestamp = datetime(2026, 2, 21, 23, 59, 56, 518662, tzinfo=timezone.utc)
        self.milestone_data = {
            "child_id": "child-123",
            "milestone_id": "milestone-123",
            "description": "Elephants",
            "completed_at": timestamp,
            "reward_generated_at": timestamp,
            "reward_url": "/milestone-123",
        }

    def test_milestone_model_instance_attributes(self):
        """ Checks that the milestone_completion_model instance atrributes
          haven't changed. Protects against drift between milestone_completion_model and 
          unit test implementation. """


        milestone = MilestoneCompletion(**self.milestone_data)
        expected_keys = ["child_id", "milestone_id", "description", "completed_at", "reward_generated_at", "reward_url", "id", "created_at", "updated_at"]
        milestone_keys = list(milestone.__dict__.keys())
        self.assertEqual(milestone_keys, expected_keys)

    @patch("app.domain.base.uuid.uuid4")
    @patch("app.domain.base.datetime")
    def test_create_a_milestone_record_and_return_dict(self, mock_timestamp, mock_uuid):
        mock_uuid.return_value = "123e4567-e89b-12d3-a456-426614174000"
        fixed_timestamp = datetime(2026, 2, 21, 23, 59, 56, 518662, tzinfo=timezone.utc)
        mock_timestamp.now.return_value = fixed_timestamp
        
        milestone = MilestoneCompletion(**self.milestone_data)
        expected_data = {
            "child_id": self.milestone_data["child_id"],
            "milestone_id": self.milestone_data["milestone_id"],
            "description": self.milestone_data["description"],
            "completed_at": fixed_timestamp,
            "reward_generated_at": fixed_timestamp,
            "reward_url": self.milestone_data["reward_url"],
            "id": mock_uuid.return_value,
            "created_at": fixed_timestamp,
            "updated_at": fixed_timestamp,
        }
        result = milestone.to_dict()
        for r in result:
            print(r, ":", result[r])
        for e in expected_data:
            print(e, ":", expected_data[e])
        self.assertEqual(milestone.to_dict(), expected_data)