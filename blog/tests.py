from django.test import TestCase

class MainPageTest(TestCase):
    def test_index_template(self):
        url = ''
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/base.html')
