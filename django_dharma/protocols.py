from typing import Protocol, runtime_checkable

from django.db import models


@runtime_checkable
class CheckProtocol(Protocol):
    """
    Protocol for defining a standard interface for model checks.

    This protocol ensures that any class implementing it has a `model` attribute of type `models.Model`
    and a `run_checks` method which performs the check and raises an exception if the check fails.

    Attributes:
        model (models.Model): The Django model instance that the checks will be performed on.

    Methods:
        run_checks() -> None:
            Executes the check on the model. If the check fails, it raises an exception. The implementation
            of this method should define the specific checks to be performed.

    Notes:
        - This protocol is used to define a common interface for different check classes that operate
          on Django models. It allows for the use of type hints and runtime type checking to ensure that
          the classes adhere to the expected interface.
        - The `@runtime_checkable` decorator allows the protocol to be checked at runtime, not just at
          type-checking time. This means that you can use `isinstance` to check if an object conforms to
          this protocol.

    Example:
        class DailyRecordCountCheck:
            model = MyModel

            def run_checks(self) -> None:
                # Implementation of the check
                ...

        check_instance = DailyRecordCountCheck()
        if isinstance(check_instance, CheckProtocol):
            check_instance.run_checks()
    """  # noqa: E501

    model: models.Model

    def run_checks(self) -> None:
        """
        Executes the check. Raises an exception if the check fails.

        This method must be implemented in a class that adheres to this protocol.
        The implementation should perform the necessary checks on the `model` attribute and raise
        an exception if the check does not pass.

        Raises:
            Exception: If the check fails, an appropriate exception should be raised.
        """  # noqa: E501
        ...
