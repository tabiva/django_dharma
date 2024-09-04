from typing import Protocol, runtime_checkable


@runtime_checkable
class CheckProtocol(Protocol):
    def run_checks(self) -> None:
        """Executes the check. Raises an exception if the check fails."""
        ...
