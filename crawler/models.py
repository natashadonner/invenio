from django.db import models


class Page(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    def __str__(self):
        return self.title
