from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Contractor(models.Model):
    name = models.CharField("название", max_length=255)
    inn = models.CharField("ИНН", max_length=12)

    class Meta:
        verbose_name = "контрагент"
        verbose_name_plural = "контрагенты"

    @property
    def slug(self):
        return slugify(self.name, allow_unicode=True) or "контрагент"

    def get_absolute_url(self):
        return reverse(
            "contractors:detail_slug", kwargs={"contractor_id": self.pk, "slug": self.slug}
        )

    def __str__(self):
        return self.name
