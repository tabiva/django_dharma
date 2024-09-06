from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from django_dharma.collector import collect_protocol_implementations
from django_dharma.protocols import CheckProtocol
from django_dharma import models


class Command(BaseCommand):
    help = "Execute checks on models"

    def handle(self, *args, **kwargs):
        for protocol in collect_protocol_implementations(CheckProtocol):
            try:
                protocol().run_checks()
                self.stdout.write(
                    self.style.SUCCESS(f"{protocol.__class__.__name__}: passed!")
                )
            except AssertionError as e:
                models.Anomaly.objects.create(
                    check_name=protocol.__class__.__name__,
                    error_message=f"{protocol.__class__.__name__}: {e}",
                    content_type=ContentType.objects.get_for_model(protocol.model),
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"{protocol.__class__.__name__}: an unexpected error occurred: {e}"
                    )
                )
