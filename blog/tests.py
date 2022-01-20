from django.test import TestCase

class MainPageTests(TestCase):
    def test_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blog/post_list.html')
