from django.core.management.base import BaseCommand
from blogs.models import Blog
class Command(BaseCommand):
    help = "Delete all blogs from the database"

    def handle(self, *args, **options):
        Blog.objects.exclude(upload_date__month=3).delete()
        self.stdout.write(self.style.SUCCESS("All blogs have been deleted successfully."))
        print("All blogs have been deleted successfully.")
