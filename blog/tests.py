from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from blog.models import Post


# Create your tests here.
class BlogTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'abednego',
            'password': '12345abcde'
        }
        self.user = User.objects.create_user(
            username=self.user_data['username'],
            password=self.user_data['password'])

        self.client.login(username=self.user_data['username'], password=self.user_data['password'])
        self.post1 = Post(title='Post 1', content='Some content for post 1', author=self.user)
        self.post1.save()
        self.post2 = Post(title='Post 2', content='Some content for post 2', author=self.user)
        self.post2.save()


    def tearDown(self):
        del self.client


    def test_create_post(self):
        data = {
            'title': 'GoT',
            'content': 'best show ever'
        }
        url = reverse('posts_create')
        self.client.post(url, data)


        posts = Post.objects.all()
        self.assertTrue(posts)