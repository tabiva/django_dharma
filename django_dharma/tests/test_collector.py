import unittest
from unittest.mock import patch, MagicMock
from django.conf import settings
from django_dharma.collector import collect_protocol_implementations
from django_dharma.protocols import CheckProtocol


# Define a mock protocol for testing
class MockProtocol(CheckProtocol):
    def run_checks(self) -> None:
        pass


# Define some mock classes for testing
class MockImplementation1(MockProtocol):
    def run_checks(self) -> None:
        pass


class MockImplementation2(MockProtocol):
    def run_checks(self) -> None:
        pass


class CollectorTestCase(unittest.TestCase):
    @patch("django_dharma.collector.importlib.import_module")
    @patch("django_dharma.collector.pkgutil.iter_modules")
    def test_collect_protocol_implementations(
        self, mock_iter_modules, mock_import_module
    ):
        # Set up mocks
        mock_module = MagicMock()
        mock_import_module.return_value = mock_module
        mock_iter_modules.return_value = [("path", "django_dharma.mock_module", "None")]
        mock_module.mock_module = MagicMock()
        mock_module.mock_module.__dict__.update(
            {
                "MockImplementation1": MockImplementation1,
                "MockImplementation2": MockImplementation2,
            }
        )

        settings.INSTALLED_APPS = ["django_dharma"]

        # Collect implementations
        result = collect_protocol_implementations(MockProtocol)

        # Assert
        self.assertIn(MockImplementation1, result)
        self.assertIn(MockImplementation2, result)
        self.assertEqual(len(result), 2)

    @patch("django_dharma.collector.importlib.import_module")
    def test_handle_module_not_found(self, mock_import_module):
        mock_import_module.side_effect = ModuleNotFoundError("Module not found")

        settings.INSTALLED_APPS = ["django_dharma"]

        # Collect implementations
        result = collect_protocol_implementations(MockProtocol)

        # Assert
        self.assertEqual(result, [])

    @patch("django_dharma.collector.importlib.import_module")
    @patch("django_dharma.collector.pkgutil.iter_modules")
    def test_handle_import_error(self, mock_iter_modules, mock_import_module):
        mock_import_module.side_effect = Exception("Import error")

        settings.INSTALLED_APPS = ["django_dharma"]

        # Collect implementations
        result = collect_protocol_implementations(MockProtocol)

        # Assert
        self.assertEqual(result, [])
