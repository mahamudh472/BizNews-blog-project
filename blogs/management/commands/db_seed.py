from blogs.models import Blog
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.utils import timezone

class Command(BaseCommand):
    help = "Duplicate existing blogs to make 10x the current number of blogs"

    def generate_unique_slug(self, title, existing_slugs):
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while slug in existing_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug  # Do not add here

    def handle(self, *args, **options):
        blogs = list(Blog.objects.all())
        original_count = len(blogs)
        if original_count == 0:
            self.stdout.write(self.style.WARNING("No blogs found to duplicate."))
            return

        target_count = original_count * 10
        to_create = target_count - original_count

        # ⚠️ Get slugs that already exist
        existing_slugs = set(Blog.objects.values_list('slug', flat=True))
        new_blogs = []

        for i in range(to_create):
            blog = blogs[i % original_count]
            title = f"{blog.title} Copy {i+1}"
            slug = self.generate_unique_slug(title, existing_slugs)
            existing_slugs.add(slug)  # ✅ Add only after generation
            new_blog = Blog(
                title=title,
                slug=slug,
                article=blog.article,
                writer=blog.writer,
                category=blog.category,
                image=blog.image,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            )
            new_blogs.append(new_blog)

        try:
            Blog.objects.bulk_create(new_blogs, ignore_conflicts=False)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error during bulk_create: {e}"))
            # Log all slugs
            for blog in new_blogs:
                self.stderr.write(f"Slug: {blog.slug}")
            return

        self.stdout.write(self.style.SUCCESS(f"Duplicated blogs. Total blogs: {Blog.objects.count()}"))
