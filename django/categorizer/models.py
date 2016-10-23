from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    label = models.CharField(max_length=128)


class Topic(models.Model):
    label = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Option(models.Model):
    label = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)
