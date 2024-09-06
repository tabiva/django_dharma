from typing import Protocol, runtime_checkable
from django.db import models


@runtime_checkable
class CheckProtocol(Protocol):
    model: models.Model

    def run_checks(self) -> None:
        """Executes the check. Raises an exception if the check fails."""
        ...
