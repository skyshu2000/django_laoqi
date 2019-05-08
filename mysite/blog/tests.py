from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import BlogArticles

class BlogDetailViewTest(TestCase):    
    def setUp(self):
        # Create one user
        user1 = User.objects.create_user(username='test1', password='!QAZ1qaz', is_superuser=True)
        user1.save()
        
        # Create one blog article
        blog_article_1 = BlogArticles.objects.create(
            title = "title 1",
            author = user1,
            body = "body 1",
        )
        blog_article_1.save()
    
    def test_blog_list(self):
        response = self.client.get(reverse('blog:blog_title'))
        self.assertEqual(response.status_code, 200)

    def test_blog_with_exist_id(self):
        """
        if the blog id exists, an appropriate message is displayed.
        """
        url = reverse('blog:blog_article', kwargs={'article_id':1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    
    def test_blog_with_not_exist_id(self):
        """
        if the blog id does NOT exist, an appropriate message is displayed.
        """
        url = reverse('blog:blog_article', kwargs={'article_id':202})        
        response = self.client.get(url)       
        self.assertEqual(response.status_code, 404)

    
