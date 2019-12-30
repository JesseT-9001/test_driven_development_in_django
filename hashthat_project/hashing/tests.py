"""
This module is used for creating functional and unit test.

To run this module use the following command:
'python manage.py test'
"""

from django.test import TestCase
from selenium import webdriver


class FunctionalTest(TestCase):
    def setUp(self) -> None:
        """
        Hook method for setting up the test fixture before exercising it.

        :var webdriver self.safari: Used to operate the safari web-browser
        :return: None
        """
        self.safari = webdriver.Safari()

    def test_there_is_a_hompage(self) -> None:
        """
        This function is used to test if there is a homepage.

        :var string localhost_8000: Holds the localhost url with port number
        :var string test_text: Hold what string you would like tested
        :except assertion: Raised if test_text is not in the page source
        :return: None
        """
        localhost_8000 = 'http://localhost:8000'
        self.safari.get(localhost_8000)

        test_text = 'install'
        self.assertIn(test_text, self.safari.page_source)

    def tearDown(self) -> None:
        """
        Hook method for deconstructing the test fixture after testing it.

        :return: None
        """
        self.safari.quit()

# def func_test():
#     """
#     :var webdriver safari: Used to operate the safari web-browser
#     :return: nothing
#     """
