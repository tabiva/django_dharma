import logging
import unittest
from io import StringIO

from core import CheckCollector, check


class CheckCollectorTestCase(unittest.TestCase):

    def setUp(self):
        """
        Setup test environment by redirecting logging output.
        """
        # Redirect log output to capture it for assertions
        self.log_stream = StringIO()
        logging.basicConfig(stream=self.log_stream, level=logging.ERROR)

    def tearDown(self):
        """
        Reset logging configuration after each test.
        """
        logging.shutdown()
        self.log_stream.close()

    def test_collects_check_methods(self):
        """
        Test that methods decorated with @check are collected correctly.
        """

        class TestChecker(CheckCollector):
            @check
            def check_one(self):
                pass

            @check
            def check_two(self):
                pass

        checker = TestChecker()
        check_methods = checker._get_check_methods()

        # Ensure both decorated methods are collected
        self.assertEqual(len(check_methods), 2)
        self.assertTrue(any(method.__name__ == "check_one" for method in check_methods))
        self.assertTrue(any(method.__name__ == "check_two" for method in check_methods))

    def test_run_all_checks_success(self):
        """
        Test that all checks run successfully without errors.
        """

        class SuccessChecker(CheckCollector):
            @check
            def check_one(self):
                assert 1 + 1 == 2, "Math error"

            @check
            def check_two(self):
                assert 2 * 2 == 4, "Multiplication error"

        checker = SuccessChecker()
        checker.run_all_checks()

        # Ensure no errors were logged
        log_output = self.log_stream.getvalue()
        self.assertEqual(log_output, "")

    def test_run_all_checks_with_failures(self):
        """
        Test that failed checks are logged correctly.
        """

        class FailureChecker(CheckCollector):
            @check
            def check_one(self):
                assert 1 + 1 == 3, "Math error"

            @check
            def check_two(self):
                assert 2 * 2 == 5, "Multiplication error"

        checker = FailureChecker()
        checker.run_all_checks()

        # Ensure both errors are logged
        log_output = self.log_stream.getvalue()
        self.assertIn("Check failed: Math error", log_output)
        self.assertIn("Check failed: Multiplication error", log_output)

    def test_unexpected_exception_handling(self):
        """
        Test that unexpected exceptions are handled and logged.
        """

        class ExceptionChecker(CheckCollector):
            @check
            def check_one(self):
                raise ValueError("Unexpected error")

        checker = ExceptionChecker()
        checker.run_all_checks()

        # Ensure the unexpected error is logged
        log_output = self.log_stream.getvalue()
        self.assertIn("Unexpected error during check check_one", log_output)
        self.assertIn("Unexpected error", log_output)


if __name__ == "__main__":
    unittest.main()
