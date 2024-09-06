from unittest.mock import patch, MagicMock
from django.conf import settings
from django.test import TestCase
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


class CollectorTestCase(TestCase):
    @patch("django_dharma.collector.importlib.import_module")
    @patch("django_dharma.collector.pkgutil.iter_modules")
    def test_collect_protocol_implementations(
        self, mock_iter_modules, mock_import_module
    ):
        # Set up a mock module with __path__
        mock_module = MagicMock()
        mock_module.__path__ = [
            "mock/path"
        ]  # This simulates the __path__ attribute of a real module

        mock_import_module.return_value = mock_module
        mock_iter_modules.return_value = [("path", "django_dharma.mock_module", False)]

        # Add the mock implementations to the mock module's __dict__
        mock_module.__dict__.update(
            {
                "MockImplementation1": MockImplementation1,
                "MockImplementation2": MockImplementation2,
            }
        )

        # Simulate INSTALLED_APPS in Django settings
        settings.INSTALLED_APPS = ["django_dharma"]

        # Collect implementations
        result = collect_protocol_implementations(MockProtocol)

        # Assert that both implementations are found
        self.assertIn(MockImplementation1, result)
        self.assertIn(MockImplementation2, result)
        self.assertEqual(len(result), 2)

    @patch("django_dharma.collector.importlib.import_module")
    def test_handle_module_not_found(self, mock_import_module):
        # Simulate a ModuleNotFoundError when importing a module
        mock_import_module.side_effect = ModuleNotFoundError("Module not found")

        # Simulate INSTALLED_APPS in Django settings
        settings.INSTALLED_APPS = ["django_dharma"]

        # Collect implementations
        result = collect_protocol_implementations(MockProtocol)

        # Assert that no implementations are found
        self.assertEqual(result, [])

    @patch("django_dharma.collector.importlib.import_module")
    @patch("django_dharma.collector.pkgutil.iter_modules")
    def test_handle_import_error(self, mock_iter_modules, mock_import_module):
        # Simulate an Exception when importing a module
        mock_import_module.side_effect = ImportError("Import error")

        # Simulate INSTALLED_APPS in Django settings
        settings.INSTALLED_APPS = ["django_dharma"]

        # Collect implementations
        result = collect_protocol_implementations(MockProtocol)

        # Assert that no implementations are found due to import error
        self.assertEqual(result, [])
