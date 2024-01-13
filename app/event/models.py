from django.db import models

class Organization(models.Model):
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
    image = models.ImageField(upload_to='vol/', null=True, blank=True)
    date = models.DateTimeField()

    def __str__(self) -> str:
        return self.title
