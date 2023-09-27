from django.db import models
from .validator import validate_robot_data


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        validators=[validate_robot_data],
    )
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
