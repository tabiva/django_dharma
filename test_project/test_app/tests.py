from django.test import TestCase
from test_app import models

from django_dharma.base import count_check
from django_dharma.models import Anomaly


class TestAppChecksTestCase(TestCase):
    def setUp(self):
        models.TestModel.objects.create(field1="field1", field2="field2")

    def test_count_check(self):
        """Assert does not trigger an exception"""
        count_check(model=models.TestModel, filters={}, count=1)
        self.assertEqual(Anomaly.objects.count(), 0)
