from django.test import TestCase
from django.urls import resolve
from blog.views import post_list

# Create your tests here.
class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_post_list_view(self):
		found = resolve('/')
		self.assertEqual(found.func, post_list)
