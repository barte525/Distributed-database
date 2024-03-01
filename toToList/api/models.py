from django.db import models


class List(models.Model):
    name = models.CharField(max_length=200)


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    list = models.ForeignKey(List, on_delete=models.CASCADE)
