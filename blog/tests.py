from django.test import TestCase
from django.urls import resolve
from blog.views import post_list
from .models import Item

# Create your tests here.
class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_post_list_view(self):
		found = resolve('/')
		self.assertEqual(found.func, post_list)

class CVPageTest(TestCase):

	def test_displays_all_list_items(self):
		Item.objects.create(title='tes_edu',text='this is test 1.')
		Item.objects.create(title='tes_edu 2',text='this is test 2.')

		response = self.client.get('/mycv/')

		self.assertIn('tes_edu', response.content.decode())
		self.assertIn('this is test 1.', response.content.decode())
		self.assertIn('tes_edu 2', response.content.decode())
		self.assertIn('this is test 2.', response.content.decode())

	def test_can_save_a_POST_request(self):
		self.client.post('/mycv/', data={'item_title': 'A new list item','item_text': 'Hello World'})

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.title, 'A new list item')
		self.assertEqual(new_item.text, 'Hello World')

	def test_redirects_after_POST(self):
		response = self.client.post('/mycv/', data={'item_title': 'A new list item','item_text': 'Hello World'})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/mycv')

	def test_only_saves_items_when_necessary(self):
		self.client.get('/mycv/')
		self.assertEqual(Item.objects.count(), 0)
