from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class Blog(models.Model):
    categories = [
        ("Politics", "Politics"),
        ("Business", "Business"),
        ("Corporate", "Corporate"),
        ("Health", "Health"),
        ("Science", "Science"),
        ("Education", "Education"),
        ("Foods", "Foods"),
        ("Entertainment", "Entertainment"),
        ("Lifestyle", "Lifestyle")
        
    ]
    title = models.CharField(max_length=200, blank=True, null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs')
    slug = AutoSlugField(populate_from='title')
    upload_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=50 ,choices=categories)
    article = CKEditor5Field(config_name='extends')
    likes =  models.IntegerField(default=0)
    comments = models.IntegerField(default=0)


    def __str__(self) -> str:
        return self.title
    