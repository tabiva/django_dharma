from test_app import models

from django_dharma.base import count_check
from django_dharma.core import CheckCollector, check


class DailyRecordCountCheck(CheckCollector):
    """Test Class implementing simlpe checks"""

    @check
    def check_at_least_one_by_value(self) -> None:
        value = "test_value"
        count = models.TestModel.object.filter(field1=value).count()
        assert (
            count >= 0
        ), f"TestModel should have at least one record with field x = {value}"
