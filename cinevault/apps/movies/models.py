from django.db import models
from cinevault.common.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
import uuid


class Movie(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    genres = models.CharField(_("Genres"), max_length=255)

    def __str__(self):
        return f"{self.title}-{self.uuid}"
