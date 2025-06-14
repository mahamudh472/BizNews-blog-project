from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Blog(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs')
    slug = AutoSlugField(populate_from='title', unique=True, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', blank=True, null=True)
    upload_date = models.DateField(auto_now_add=True)
    article = CKEditor5Field(config_name='extends')
    likes =  models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']


    def __str__(self) -> str:
        return self.title if self.title else 'No Title'


