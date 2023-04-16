from django.db import models


# Create your models here.
class student(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    number = models.CharField(max_length=11)


class urls(models.Model):
    long_urls = models.TextField()
    short_urls = models.CharField(max_length=20)
