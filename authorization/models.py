from django.db import models
from django.utils.text import slugify
from django.utils.timezone import now
from django.shortcuts import reverse
import uuid


from profiles.models import Creator

status = (
        ('dr' ,'Draft'),
        ('pub', 'Published'),
        ('del', 'Deleted')
    )

class Post(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(blank=True, max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=now, blank=True)
    status = models.CharField(
        choices=status,
        max_length=3, 
        default='dr',
        blank=True,
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Creator, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=10000)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('authorization-detail-post', kwargs={
            'slug': self.slug,
            'uuid': self.uuid,
        })

    def __str__(self):
        return self.title


class Review(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(blank=True, max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=now, blank=True)
    status = models.CharField(
        choices=status,
        max_length=3,
        default='dr',
        blank=True,
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Creator, on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=10000)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('authorization-detail-review', kwargs={
            'slug': self.slug,
            'uuid': self.uuid,
        })

    def __str__(self):
        return self.title
