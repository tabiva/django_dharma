from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from django_dharma.models import Anomaly


class AnomalyModelTest(TestCase):
    def setUp(self):
        """Set up the test data."""
        self.content_type = ContentType.objects.create(
            app_label="test_app", model="testmodel"
        )
        self.anomaly = Anomaly.objects.create(
            check_name="Test Check",
            model_name="TestModel",
            content_type=self.content_type,
            error_message="Test error message",
        )

    def test_anomaly_creation(self):
        """Test that the anomaly is created and saved correctly."""
        self.assertTrue(Anomaly.objects.filter(id=self.anomaly.id).exists())

    def test_anomaly_fields(self):
        """Test that the anomaly fields are saved correctly."""
        anomaly = Anomaly.objects.get(id=self.anomaly.id)
        self.assertEqual(anomaly.check_name, "Test Check")
        self.assertEqual(anomaly.model_name, "TestModel")
        self.assertEqual(anomaly.error_message, "Test error message")
        self.assertEqual(anomaly.content_type, self.content_type)

    def test_anomaly_str(self):
        """Test the string representation of the anomaly."""
        expected_str = f"Test Check - TestModel at {self.anomaly.timestamp}"
        self.assertEqual(str(self.anomaly), expected_str)
