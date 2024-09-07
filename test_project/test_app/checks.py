from test_app import models

from django_dharma.base import count_check


class TestAppChecks:
    def run_checks(self) -> None:
        """
        Checks that there are 10 records of TestModel
        """
        count_check(model=models.TestModel, filters={}, count=10)
