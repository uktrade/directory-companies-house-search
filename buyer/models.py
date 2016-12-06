from directory_validators.constants import choices

from django.db import models

from api.model_utils import TimeStampedModel


class Buyer(TimeStampedModel):

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    sector = models.CharField(
        choices=choices.COMPANY_CLASSIFICATIONS,
        max_length=255,
    )

    def __str__(self):
        return self.name
