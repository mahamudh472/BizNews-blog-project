from django.core.management.base import BaseCommand
from blogs.models import Blog
from django.db.models import Count

class Command(BaseCommand):
    help = 'Delete duplicate blog posts based on slug'

    def handle(self, *args, **kwargs):
        duplicates = (
            Blog.objects.values('slug')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        total_deleted = 0
        for dup in duplicates:
            posts = Blog.objects.filter(slug=dup['slug']).order_by('created_at')  # Keep oldest
            posts_to_delete = posts[1:]  # Exclude the first one
            deleted_count, _ = posts_to_delete.delete()
            total_deleted += deleted_count
            self.stdout.write(f"Deleted {deleted_count} posts with slug: {dup['slug']}")

        self.stdout.write(self.style.SUCCESS(f"Duplicate deletion completed. Total deleted: {total_deleted}"))
