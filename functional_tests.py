from selenium import webdriver
from time import sleep
import unittest
import re

class NewVisitorTest(unittest.TestCase):  

    def setUp(self):  
        self.browser = webdriver.Safari()

    def tearDown(self):  
        self.browser.quit()

    def test_basic_functions(self):  
        # Open up the blog website
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # Retrieve current url
        URL = self.browser.current_url

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

        # Check the 'Resume' page linked homepage
        self.browser.find_element_by_class_name('nav__link3').click()
        sleep(1)
        cv_text = self.browser.find_element_by_tag_name('p').text
        self.assertIn('I am keen to view somewhere far enough and wide enough.', cv_text)

        # Clicking the header icon can go back to its homepage
        self.browser.find_element_by_class_name('menu-logo').click()
        sleep(1)

        # Should be back homepage
        self.assertEquals(URL, 'http://localhost:8000/')

    def test_dark_mode(self):
        self.browser.get('http://localhost:8000')

        body = self.browser.find_element_by_css_selector('body').value_of_css_property('background-color')
        r0,g0,b0 = map(int, re.search(
             r'rgb\((\d+),\s*(\d+),\s*(\d+)', body).groups())
        white = '#%02x%02x%02x' % (r0, g0, b0)

        self.assertEquals('#ffffff', white)

        self.browser.find_element_by_link_text('Darken').click()
        sleep(1)

        darkened_body = self.browser.find_element_by_css_selector('body').value_of_css_property('background-color')
        r1,g1,b1 = map(int, re.search(
             r'rgb\((\d+),\s*(\d+),\s*(\d+)', darkened_body).groups())
        black = '#%02x%02x%02x' % (r1, g1, b1)

        self.browser.find_element_by_link_text('About').click()
        sleep(1)

        self.assertEquals('#0c090a', black)

        darkened_body_at_another_url = self.browser.find_element_by_css_selector('body').value_of_css_property('background-color')
        r2,g2,b2 = map(int, re.search(
             r'rgb\((\d+),\s*(\d+),\s*(\d+)', darkened_body_at_another_url).groups())
        black_again = '#%02x%02x%02x' % (r2, g2, b2)

        self.assertEquals(black, black_again)

        self.browser.find_element_by_link_text('Darken').click()
        sleep(1)

        lightened_body = self.browser.find_element_by_css_selector('body').value_of_css_property('background-color')
        r3,g3,b3 = map(int, re.search(
             r'rgb\((\d+),\s*(\d+),\s*(\d+)', lightened_body).groups())
        white_again = '#%02x%02x%02x' % (r3, g3, b3)
        sleep(1)

        self.assertEquals(white, white_again)

        # error here
        #self.browser.find_element_by_class_name('dark-mode-button').click()
        #sleep(1)
        #self.browser.find_element_by_class_name('dark-mode-button').click()
        #sleep(1)



if __name__ == '__main__':  
    unittest.main()  