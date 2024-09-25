import logging
from typing import Callable, List, Iterator
from django.contrib.contenttypes.models import ContentType
from django_dharma import models


logging.basicConfig(level=logging.ERROR)


def check(method: Callable) -> Callable:
    """
    Decorator to mark a method as a check method and handle exceptions.

    This decorator logs AssertionError and unexpected exceptions while allowing the
    execution of other checks to continue.
    """

    def wrapper(*args, **kwargs):
        try:
            method(*args, **kwargs)
        except AssertionError as e:
            class_name = args[0].__class__.__name__
            method_name = method.__name__

            models.Anomaly.objects.create(
                check_name=f"{method_name}.{class_name}",
                error_message=e,
            )

            logging.error(f"Check failed: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during check {method.__name__}: {e}")

    wrapper._is_check = True
    return wrapper


class CheckCollector:
    """
    Base class that collects and executes all methods marked with the @check decorator.

    This class serves as a foundation for creating model validation or check classes.
    Any method decorated with `@check` will be executed when `run_all_checks()` is called.
    Errors (such as AssertionError) raised during check execution will be caught and logged,
    allowing other checks to continue running.

    Attributes:
        None
    """

    def run_checks(self) -> None:
        """
        Execute all methods decorated with @check.

        This method retrieves all methods marked as checks using the `_get_checks()`
        helper function. Each check is executed sequentially.

        Raises:
            None
        """
        for check in list(self._get_checks()):
            check()

    def _get_checks(self) -> Iterator[Callable]:
        """
        Retrieve all methods decorated with @check.

        This method inspects the current instance and yields all callable
        methods that have been decorated with `@check` by checking for the `_is_check`
        attribute.

        Yields:
            Callable: A check method to be executed.
        """
        for attr_name in dir(self):
            if (
                (attr := getattr(self, attr_name))
                and callable(attr)
                and getattr(attr, "_is_check", False)
            ):
                yield attr
