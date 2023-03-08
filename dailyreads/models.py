
from django.db import models
import uuid
# Create your models here.


class Blogs(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    target_link = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4(),primary_key=True,editable=False,unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Blogs'


class News(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    target_link = models.CharField(max_length=200)
    id = models.UUIDField(default=uuid.uuid4(),primary_key=True, editable=False,unique=True)
    created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'News'


class Quote(models.Model):
    quote_text = models.CharField(max_length=500)
    author = models.CharField(max_length=100,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

