from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from django_dharma.core import CheckCollector, check


class DailyRecordCountCheck(CheckCollector):
    """Test Class implementing simlpe checks"""

    @check
    def check_positive_records(self) -> None:
        assert 1 + 1 == 2, "Basic math error: 1 + 1 should be 2"

    @check
    def check_no_division_by_zero(self) -> None:
        assert 1 / 1 == 2, "Fake failing test"

    @check
    def check_even_number(self) -> None:
        assert 4 % 2 == 0, "4 is not an even number"


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        DailyRecordCountCheck().run_checks()
