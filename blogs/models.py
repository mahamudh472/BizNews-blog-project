from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    def get_blogs_count(self):
        return self.blogs.count()
    
class Blog(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blogs')
    slug = AutoSlugField(populate_from='title', unique=True, max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs', blank=True, null=True)
    upload_date = models.DateField(auto_now_add=True)
    article = CKEditor5Field(config_name='extends')
    likes =  models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']


    def __str__(self) -> str:
        return self.title if self.title else 'No Title'
    
    def get_comments(self):
        return self.comment_set.all()


class Comment(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.blog.title}'
    def get_replies(self):
        return self.replies.all()

class BlogView(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'user')

    def __str__(self):
        return f'View by {self.user.username} on {self.blog.title}'
