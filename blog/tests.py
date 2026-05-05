from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from .models import Post

class BlogTests(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(
            title='Testowy Post',
            content='Treść testowa',
            author=self.user
        )

    def test_post_content(self):
        post = Post.objects.get(id=self.post.id)
        self.assertEqual(post.title, 'TO JEST CELOWY BLAD')

    def test_homepage_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)