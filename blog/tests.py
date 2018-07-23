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

    def test_list_posts(self):
        url = reverse('posts_list')
        response = self.client.get(url)

        self.assertInHTML('<p>Some content for post 1</p>', str(response.content), count=1)
        self.assertInHTML('<p>Some content for post 2</p>', str(response.content), count=1)
    

    def test_update_post(self):
        url = reverse('posts_edit', kwargs={'pk': self.post1.id })
        response = self.client.get(url)
        self.assertContains(response, 'Some content for post 1', count=1)

        edits = {
            'title': 'New title for post 1',
            'content': 'New content for post 1'
        }
        response = self.client.post(url, edits)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/'))


    def test_delete_post(self):
        url = reverse('posts_delete', kwargs={'pk': self.post1.id })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)


    