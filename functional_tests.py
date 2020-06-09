from selenium import webdriver
from time import sleep
import unittest

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Safari()

    def tearDown(self):  
        self.browser.quit()

    def test_basic_functions(self):  
        # Open up the blog website
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # Check the page title and header mention Wenyue lists
        self.assertIn('Wenyue', self.browser.title)  
        header_text = self.browser.find_element_by_tag_name('h1').text  
        self.assertIn('Wenyue', header_text)
        footer_text = self.browser.find_element_by_tag_name('footer').text
        self.assertIn('Designed by',footer_text)

        # Check the 'About' page linked homepage
        self.browser.find_element_by_link_text('About').click()
        sleep(1)
        about_text = self.browser.find_element_by_tag_name('p').text
        self.assertIn('This is the website of Wenyue Jin.', about_text)

        # Clicking the header icon can go back to its homepage
        self.browser.find_element_by_class_name('menu-icon').click()
        sleep(1)
        
        

if __name__ == '__main__':  
    unittest.main()  