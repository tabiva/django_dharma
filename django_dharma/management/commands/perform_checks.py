from collector import collect_protocol_implementations
from django.core.management.base import BaseCommand
from protocols import CheckProtocol


class Command(BaseCommand):
    help = "Execute checks on models"

    def handle(self, *args, **kwargs):
        for protocol in collect_protocol_implementations(CheckProtocol):
            try:
                protocol.run_checks()
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{protocol.__class__.__name__}: superato con successo."
                    )
                )
            except AssertionError as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"{protocol.__class__.__name__}: errore nei controlli: {e}"
                    )
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f"{protocol.__class__.__name__}: si è verificato un errore imprevisto: {e}"
                    )
                )
