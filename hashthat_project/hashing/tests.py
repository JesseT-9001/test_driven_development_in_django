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

        :var string test_text: Hold what string you would like tested
        :except assertion: Raised if test_text is not in the page source

        :return: None
        """
        self.__open_homepage()

        test_text = 'Enter hash here:'
        self.assertIn(test_text, self.safari.page_source)

    def test_hash_of_hello(self) -> None:
        """
        This function inputs the text 'hello' and checks if the output hash is correct

        :var string element_id: Contains an element id in the form of a string
        :var string test_text: Contains a string to input
        :var string element_name: Contains an element name in the form of a string
        :var string hash_test: Contains a hash value in the form of a string

        :return: None
        """
        self.__open_homepage()

        element_id = 'id_text'
        text = self.safari.find_element_by_id(element_id)

        test_text = 'hello'
        text.send_keys(test_text)

        element_name = 'submit'
        self.safari.find_element_by_name(element_name).click()

        hash_test = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        self.assertIn(hash_test, self.safari.page_source)

    def __open_homepage(self) -> None:
        """
        This function opens the homepage.

        :var string url: Holds the url with port number as a string

        :return: None
        """
        url = 'http://localhost:8000'
        self.safari.get(url)

    def tearDown(self) -> None:
        """
        Hook method for deconstructing the test fixture after testing it.

        :return: None
        """
        self.safari.quit()


class UnitTest(TestCase):
    pass
