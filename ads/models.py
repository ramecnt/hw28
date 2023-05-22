from django.db import models


class Ads(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=2000)
    address = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)
