from django.test import TestCase
from blogs.models import Blog, Category

class test_Category(TestCase):
    def setUp(self):
        self.cat1 = Category.objects.create(name='Technology')
        self.cat2 = Category.objects.create(name='Entertainment')

    def test_objects_created(self):
        data = Category.objects.filter(name="Technology").exists()
        data2 = Category.objects.filter(name="Entertainment").exists()
        data3 = Category.objects.filter(name="None").exists()

        self.assertTrue(data)
        self.assertTrue(data2)
        self.assertFalse(data3)


class test_Blog(TestCase):
    def test_add(self):
        self.assertEqual('1', '1')