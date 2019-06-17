from django.db import models
from django.contrib.postgres.fields import JSONField

from scrap.models import Company

class Analisys(models.Model):

    class Meta:
        verbose_name_plural = 'Analysis'
        unique_together = ['company', 'kernel', 'svm', 'number_of_days_sample', 'number_of_train_vectors']

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='companies'
    )

    kernel = models.CharField(
        help_text="Kernel of the SVM",
        max_length=100,
        null=True,
        blank=True
    )

    svm = models.CharField(
        help_text="SVM type",
        max_length=100,
        null=True,
        blank=True
    )

    rate = models.FloatField(
        null=True,
        blank=True
    )

    number_of_days_sample = models.IntegerField(
        null=True,
        blank=True
    )

    number_of_train_vectors = models.IntegerField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Creation time",
    )
