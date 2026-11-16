from django.db import models


class Contractor(models.Model):
    name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12)

    def __str__(self):
        return self.name
