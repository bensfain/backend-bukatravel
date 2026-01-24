from django.db import models
from solo.models import SingletonModel


class TemplateConfig(SingletonModel):
    site_name = models.CharField(max_length=50, default="Site Name")

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
