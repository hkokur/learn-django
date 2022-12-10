from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import uuid


class Profile(models.Model):
    user = models.OneToOneField(to = get_user_model(), on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    slug = models.SlugField(blank=True)
    first_name = models.CharField(max_length=200,blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to = "profile_pictures/", blank=True, null=True)

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def save(self, *args, **kwargs):
        if not self.slug :
            self.slug = slugify(self.user.username)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Creator(models.Model):
    profile = models.OneToOneField(to = Profile, on_delete=models.CASCADE)
    number_of_content = models.PositiveSmallIntegerField(default=0)
    salary = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = "creator"
        verbose_name_plural = "creators"

    def __str__(self):
        return self.profile.user.username


class Editor(models.Model):
    profile = models.OneToOneField(to = Profile, on_delete=models.CASCADE)
    number_of_edited_content = models.PositiveSmallIntegerField(default=0)
    salary = models.PositiveIntegerField()
    
    class Meta:
        verbose_name = "editor"
        verbose_name_plural = "editors"
    
    def __str__(self):
        return self.profile.user.username
