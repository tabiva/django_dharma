from django.contrib.contenttypes.models import ContentType
from django.db import models


class Anomaly(models.Model):
    check_name = models.CharField(max_length=255)
    model_name = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    error_message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.check_name} - {self.model_name} at {self.timestamp}"
