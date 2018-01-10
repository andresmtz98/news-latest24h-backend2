from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=10000000)
    source = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    urlImage = models.CharField(max_length=255)
    publishedAt = models.CharField(max_length=255)
