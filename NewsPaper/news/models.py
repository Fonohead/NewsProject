from django.db import models


class Category(models.Model):
    category_title = models.CharField(max_length=255, unique=True)

class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()





