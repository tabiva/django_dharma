from django.db import models


def count_check(model: models.base.ModelBase, filters: dict, count: int) -> None:
    """
    Checks that the number of records in the model that match the filters is
    greater than or equal to the specified number. Raises an exception if the check fails.

    :param model: Django model to perform the check on.
    :param filters: Dictionary of filters to apply to the model's records.
    :param count: Minimum number of expected records.
    """  # noqa: E501
    tot = model.objects.filter(**filters).count()

    assert tot >= count, (
        f"Check failed: {model.__name__} has {tot} records "
        f"matching the filters {filters}, but at least {count} were expected."
    )

    print(
        f"Check passed: {model.__name__} has {tot} records "
        f"matching the filters {filters}."
    )
