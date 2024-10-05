from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from datetime import datetime

from django.db.models import Sum
from django.db.models.functions import Coalesce

from django.core.validators import MinValueValidator
from django.urls import reverse

from django.core.cache import cache

from django.utils.translation import gettext_lazy as _

from protect.models import User


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.name.title()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    text = RichTextUploadingField()
    create_time = models.DateTimeField(auto_now_add = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.header.capitalize()



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    comm_text = models.TextField(default=False)
    COMMENT_STATUS = [('pending', 'на рассмотрении'), ('accepted', 'принят'),
                      ('rejected', 'отклонен')]
    status = models.CharField(max_length=10, choices=COMMENT_STATUS, default='pending')


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.comm_text[:30] if len(self.comm_text) > 30 else self.comm_text


    def __str__(self):
        return f'{self.create_time}: {self.comm_text}: {self.user}: {self.status}'



