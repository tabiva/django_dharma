from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from django_dharma import models
from django_dharma.collector import collect_protocol_implementations
from django_dharma.protocols import CheckProtocol


class Command(BaseCommand):
    """
    A Django management command to execute checks on models based on
    implementations of the CheckProtocol interface.

    This command collects all protocol implementations of CheckProtocol,
    executes their `run_checks` method, and reports the results.
    Successful checks are reported as passed, while anomalies and errors
    are logged as Django model instances and error messages respectively.

    Usage:
        python manage.py <command_name>
    """

    help = "Execute checks on models"

    def handle(self, *args, **kwargs):
        """
        Collects protocol implementations of CheckProtocol and executes
        their `run_checks` method.

        For each protocol:
        - Calls the `run_checks` method.
        - Logs a success message if no errors are encountered.
        - Creates an Anomaly record in the database if an AssertionError is raised.
        - Logs an error message for any unexpected exceptions.

        Arguments:
            *args: Additional positional arguments passed to the command.
            **kwargs: Additional keyword arguments passed to the command.
        """  # noqa: E501
        for protocol in collect_protocol_implementations(CheckProtocol):
            try:
                # Execute the protocol's checks
                protocol().run_checks()
                self.stdout.write(
                    self.style.SUCCESS(f"{protocol.__class__.__name__}: passed!")
                )
            except AssertionError as e:
                # Log an anomaly if an AssertionError is raised
                print(protocol.model.__doc__)
                models.Anomaly.objects.create(
                    check_name=protocol.__class__.__name__,
                    error_message=f"{protocol.__class__.__name__}: {e}",
                    content_type=ContentType.objects.get_for_model(protocol.model),
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{protocol.__class__.__name__}: Anomalies found (and logged)!"
                    )
                )
            except Exception as e:
                # Log an unexpected error
                self.stdout.write(
                    self.style.ERROR(
                        f"{protocol.__class__.__name__}: an unexpected error occurred: {e}"  # noqa: E501
                    )
                )
