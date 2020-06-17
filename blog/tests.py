from django.test import TestCase
from django.urls import resolve
from blog.views import post_list
from .models import *
from django.contrib.auth.models import User

# Create your tests here.
class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_post_list_view(self):
		found = resolve('/')
		self.assertEqual(found.func, post_list)

class PostTest(TestCase):

	def test_displays_all_posts(self):
		u = User.objects.create_user('Chevy Chase','chevyspassword')
		Post.objects.create(author=u,title='This is a test post.',text='hello',created_date='1999-01-01',published_date='1999-01-01')
		Post.objects.create(author=u,title='Oh no.',text='world',created_date='1999-01-01',published_date='1999-01-01')
		response = self.client.get('/')
		self.assertIn('This is a test post', response.content.decode())
		self.assertIn('hello', response.content.decode())
		self.assertIn('Oh', response.content.decode())
		self.assertIn('world', response.content.decode())


class CVPageTest(TestCase):

	def test_displays_all_items_in_edu_field(self):
		Item.objects.create(title='test_edu',text='this is test 1.')
		Item.objects.create(title='test_edu 2',text='this is test 2.')

		response = self.client.get('/mycv/')

		self.assertIn('test_edu', response.content.decode())
		self.assertIn('this is test 1.', response.content.decode())
		self.assertIn('test_edu 2', response.content.decode())
		self.assertIn('this is test 2.', response.content.decode())

	def test_displays_all_items_in_intern_field(self):
		Intern.objects.create(start_date='1999-06-01',end_date='1999-12-01', text='Hi.')
		Intern.objects.create(start_date='1999-01-02',end_date='1999-02-02', text='Bye.')

		response = self.client.get('/mycv/')

		self.assertIn('June', response.content.decode())
		self.assertIn('Dec.', response.content.decode())
		self.assertIn('Hi.', response.content.decode())
		self.assertIn('Jan', response.content.decode())
		self.assertIn('Feb', response.content.decode())
		self.assertIn('Bye.', response.content.decode())

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

class ModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

    def test_saving_and_retrieving_interns(self):
        first_item = Intern()
        first_item.text = 'The first (ever) list item'
        first_item.start_date = '1999-01-01'
        first_item.end_date = '2000-01-01'
        first_item.save()

        second_item = Intern()
        second_item.text = 'Item the second'
        second_item.start_date = '1999-02-01'
        second_item.end_date = '2000-02-01'
        second_item.save()

        saved_items = Intern.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        fsd = first_saved_item.start_date
        f_start_date = fsd.strftime("%Y-%m-%d")
        fed = first_saved_item.end_date
        f_end_date = fed.strftime("%Y-%m-%d")
        ssd = second_saved_item.start_date
        s_start_date = ssd.strftime("%Y-%m-%d")
        sed = second_saved_item.end_date
        s_end_date = sed.strftime("%Y-%m-%d")

        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(f_start_date, '1999-01-01')
        self.assertEqual(f_end_date, '2000-01-01')
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(s_start_date, '1999-02-01')
        self.assertEqual(s_end_date, '2000-02-01')

class CommentTest(TestCase):

	def test_displays_all_items_above(self):
		Comment.objects.create(name='Mark Lee',text='No exam in the third year.')
		Comment.objects.create(name='Bruce Lee',text='Adaaaaaaaa.')

		response = self.client.get('/comment/')

		self.assertIn('Mark Lee', response.content.decode())
		self.assertIn('No exam ', response.content.decode())
		self.assertIn('Bruce Lee', response.content.decode())
		self.assertIn('aaaaa', response.content.decode())

	def test_only_saves_items_when_necessary(self):
		self.client.get('/comment/')
		self.assertEqual(Item.objects.count(), 0)

	def test_can_save_a_POST_request(self):
		response = self.client.post('/comment/', data={'nickname': 'Mark Lee','text': 'No exam in the third year.'})

		self.assertEqual(Comment.objects.count(), 1)
		fst = Comment.objects.first()
		self.assertEqual(fst.name, 'Mark Lee')
		self.assertEqual(fst.text, 'No exam in the third year.')
		self.assertEqual(response.status_code, 200)