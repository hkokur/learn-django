from django.db import models
from django.utils.text import slugify

STATUS = [
    ("dr", "draft"),
    ("pu", "published"),
    ("de","deleted")
]

class Post(models.Model):
    status = models.CharField(max_length=2,choices=STATUS, default="dr")
    title = models.CharField(max_length=100)
    update = models.DateField(auto_now=True)
    create = models.DateField(auto_now_add=True)
    author = models.ForeignKey(
        "auth.user",
        on_delete=models.SET_NULL,
        blank = True,
        null = True
    )
    content = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

