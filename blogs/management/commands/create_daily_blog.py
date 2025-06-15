from django.core.management.base import BaseCommand
from blogs.models import Blog, Category
from django.contrib.auth.models import User
from django.utils import timezone
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Create a new blog every day (for cron job)'

    def handle(self, *args, **kwargs):
        faker = Faker()
        # Get or create a random user
        user = User.objects.order_by('?').first()
        if not user:
            self.stdout.write(self.style.ERROR('No users found.'))
            return
        # Get or create a random category
        category = Category.objects.order_by('?').first()
        if not category:
            category = Category.objects.create(name=faker.word())
        title = faker.sentence(nb_words=6)
        article = '<br>'.join(faker.paragraphs(nb=random.randint(3, 7)))
        blog = Blog.objects.create(
            title=title,
            writer=user,
            image='blogs/default.jpg',  # You may want to set a default image
            category=category,
            article=article,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
        self.stdout.write(self.style.SUCCESS(f'Created blog: {blog.title}'))
