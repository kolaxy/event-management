from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL


class Organization(models.Model):
    founder = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='founded_organizations'
    )
    members = models.ManyToManyField(
        User,
        related_name='organizations',
        blank=True,
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    postcode = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    organizations = models.ManyToManyField(Organization)
    image = models.ImageField(
        upload_to='vol/',
        null=True,
        blank=True
    )
    date = models.DateTimeField()

    def __str__(self) -> str:
        return self.title
