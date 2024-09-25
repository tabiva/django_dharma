from test_app import models

from django_dharma.base import count_check


class TestAppChecks:
    model = models.TestModel

    def run_checks(self) -> None:
        """
        Checks that there are 10 records of TestModel
        """
        count_check(model=self.model, filters={}, count=10)
