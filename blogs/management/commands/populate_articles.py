from django.core.management.base import BaseCommand
from blogs.models import Blog, Category
import faker as fack
import random

class Command(BaseCommand):
    help = 'Populate the database with sample articles'

    def handle(self, *args, **kwargs):
        blogs = Blog.objects.all()
        counter = 0
        self.stdout.write(self.style.SUCCESS(f'Found {blogs.count()} blogs to populate articles.'))
        faker = fack.Faker()
        for blog in blogs:
            paragraphs = [faker.paragraph(nb_sentences=random.randint(4, 7)) for _ in range(random.randint(3, 6))]
            content = '\n\n'.join(paragraphs)
            content = content.replace('\n', '<br>')
            blog.article = content
            blog.save()
            counter += 1
            self.stdout.write(self.style.SUCCESS(f'{counter}. Successfully populated article for blog: {blog.title}'))
        self.stdout.write(self.style.SUCCESS(f'Successfully populated articles for {counter} blogs.'))
