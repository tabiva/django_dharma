from django.contrib.contenttypes.models import ContentType
from django.db import models


class Anomaly(models.Model):
    """
    Represents an anomaly detected during the execution of checks in the system.

    Fields:
        check_name (CharField): The name of the check that raised the anomaly.
                                This field stores a description or identifier of the check.
        model_name (CharField): The name of the model where the anomaly was detected.
                                Typically, this would be the string representation of the Django model's class name.
        content_type (ForeignKey): A reference to the ContentType of the model where the anomaly occurred.
                                   This allows for generic relations to any model in the system.
        error_message (TextField): A detailed description of the error or anomaly detected during the check.
        timestamp (DateTimeField): The timestamp when the anomaly was detected, automatically set to the
                                   current date and time when the record is created.

    Methods:
        __str__(): Returns a string representation of the anomaly in the format:
                   "<check_name> - <model_name> at <timestamp>".

    Usage:
        This model is useful for logging and tracking anomalies encountered during model checks in your application.
        The use of `ContentType` allows for flexible referencing of different models without tightly coupling
        to any specific one.

    Example:
        anomaly = Anomaly.objects.create(
            check_name='Daily Record Count',
            model_name='MyModel',
            content_type=ContentType.objects.get_for_model(MyModel),
            error_message='Expected at least 30 records, but found 20.'
        )
        print(anomaly)  # Output: Daily Record Count - MyModel at 2023-09-05 12:00:00
    """  # noqa: E501

    check_name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    error_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.check_name} - {self.model_name} at {self.timestamp}"
