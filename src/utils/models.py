"""Django models utilities."""

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    """Base model.

    BaseModel acts as an abstract base class from which every
    other model in the project will inherit. This class provides
    every table with the following attributes:
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        help_text='Date time on which the object was created.'
    )
    modified = models.DateTimeField(
        _('modified at'),
        auto_now=True,
        help_text='Date time on which the object was last modified.'
    )

    class Meta:
        """Meta option."""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']