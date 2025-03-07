from blogs.models import Category, Blog
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
# for item in categories:
#     print(item)
#     Category.objects.create(name=item[0])
from django.contrib.auth.models import User
import json
user = User.objects.first()
with open('data.json', 'r') as f:
    d = json.load(f)
    for item in d:
        Blog.objects.create(
            title=item['title'],
            writer=user,
            image=item['image_url'],
            article=item['content']
        )
