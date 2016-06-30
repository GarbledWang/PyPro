from django.db import models

# Create your models here.
class User:
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    def __unicode__(self):
        return self.username


class Article:
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=30)
    date = models.DateField()
    content = models.TextField()