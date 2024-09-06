import unittest
from django_dharma.protocols import CheckProtocol
from django.db import models


# Mock valid check that should conform to CheckProtocol
class ValidCheck:
    model = models.Model

    def run_checks(self) -> None:
        pass


# Mock invalid check that should not conform to CheckProtocol
class InvalidCheck:
    pass  # This class does not implement run_checks or have model attribute


class ProtocolTestCase(unittest.TestCase):

    def test_check_protocol_incompatibility(self):
        """
        Test that InvalidCheck does not conform to CheckProtocol.
        """
        check_instance = InvalidCheck()
        # Ensure the class does not conform to CheckProtocol by checking isinstance
        self.assertNotIsInstance(
            check_instance,
            CheckProtocol,
            "InvalidCheck should not conform to CheckProtocol",
        )

    def test_check_protocol_method_presence(self):
        """
        Test that ValidCheck has the required methods.
        """
        check_instance = ValidCheck()
        # Ensure that run_checks is callable
        self.assertTrue(
            callable(check_instance.run_checks), "run_checks should be callable"
        )
        # Ensure the model attribute is present
        self.assertTrue(
            hasattr(check_instance, "model"), "model attribute should be present"
        )
