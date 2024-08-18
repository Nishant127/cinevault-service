from django.db import models
from cinevault.common.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from users.models import User
from movies.models import Movie
import uuid


class MovieCollection(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="collections", verbose_name=_("User"))
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_("Title"), max_length=255)
    description = models.TextField(_("Description"))
    movies = models.ManyToManyField(Movie, related_name="collections", verbose_name=_("Movies"))

    def __str__(self):
        return f"{self.user}-{self.title}"
