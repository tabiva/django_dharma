from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django_dharma.models import Anomaly
from django.db import models


# Mock model for testing
class MockModel(models.Model):
    pass


class AnomalyModelTestCase(TestCase):
    def setUp(self):
        """Set up test data."""
        self.mock_model = MockModel.objects.create()
        self.content_type = ContentType.objects.get_for_model(self.mock_model)

    def test_anomaly_creation(self):
        """Test that an anomaly can be created and saved."""
        anomaly = Anomaly.objects.create(
            check_name="Test Check",
            model_name="MockModel",
            content_type=self.content_type,
            error_message="Test error message.",
        )
        self.assertEqual(Anomaly.objects.count(), 1)
        self.assertEqual(anomaly.check_name, "Test Check")
        self.assertEqual(anomaly.model_name, "MockModel")
        self.assertEqual(anomaly.content_type, self.content_type)
        self.assertEqual(anomaly.error_message, "Test error message.")

    def test_anomaly_str(self):
        """Test the string representation of the anomaly."""
        anomaly = Anomaly.objects.create(
            check_name="Test Check",
            model_name="MockModel",
            content_type=self.content_type,
            error_message="Test error message.",
        )
        expected_str = f"Test Check - MockModel at {anomaly.timestamp}"
        self.assertEqual(str(anomaly), expected_str)
