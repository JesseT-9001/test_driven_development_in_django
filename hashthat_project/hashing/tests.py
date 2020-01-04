"""
This module is used for creating functional and unit tests.

To run this module use the following command:
'python manage.py test'
"""

from django.test import TestCase
from selenium import webdriver
from .forms import HashForm
import hashlib
from .models import *
from django.core.exceptions import ValidationError
import time


class FunctionalTest(TestCase):
    def setUp(self) -> None:
        """
        Hook method for setting up the test fixture before exercising it.

        :var webdriver self.safari: Used to operate the safari web-browser

        :return: None
        """
        self.browser = webdriver.Chrome()

    def test_there_is_a_hompage(self) -> None:
        """
        This function is used to test if there is a homepage.

        :var string test_text: Hold what string you would like tested

        :except assertion: Raised if test_text is not in the page source

        :return: None
        """
        self.open_homepage()

        test_text = 'Enter hash here:'
        self.assertIn(test_text, self.browser.page_source)

    def test_hash_of_hello(self) -> None:
        """
        This function inputs the text 'hello' and checks if the output hash is correct

        :var string element_id: Contains an element id in the form of a string
        :var string test_text: Contains a string to input
        :var string element_name: Contains an element name in the form of a string
        :var string hash_test: Contains a hash value in the form of a string

        :return: None
        """
        self.open_homepage()

        element_id = 'id_text'
        text = self.browser.find_element_by_id(element_id)

        test_text = 'hello'
        text.send_keys(test_text)

        element_name = "submit"
        self.browser.find_element_by_name(element_name).click()

        hash_test = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
        self.assertIn(hash_test, self.browser.page_source)

    def test_hash_ajax(self):
        """
        Uses time module to sleep and wait for ajax.

        :var arrary test: Array of test variables
        :var string text: allows focus to be put on textarea.

        :except assertion: Raised if correct hash is not found in page source

        :return: None
        """
        self.open_homepage()
        test = hash_to_test()
        text = self.browser.find_element_by_id(test[3])
        text.send_keys(test[0])
        time.sleep(5)
        self.assertIn(test[2], self.browser.page_source)

    def open_homepage(self) -> None:
        """
        This function opens the homepage.

        :var string url: Holds the url with port number as a string

        :return: None
        """
        url = 'http://localhost:8000'
        self.browser.get(url)

    def tearDown(self) -> None:
        """
        Hook method for deconstructing the test fixture after testing it.

        :return: None
        """
        self.browser.quit()


class UnitTest(TestCase):

    def test_home_homepage_template(self):
        """
        :var string home_url: holds the url to the homepage.
        :var response response: holds a get response.
        :var string home_template: holds the template location of the homepage template

        :except assertion: Raised if template homepage is not found.

        :return: None
        """
        home_url = '/'
        response = self.create_response(home_url)

        home_template = 'home.html'
        self.assertTemplateUsed(response, home_template)

    def test_hash_form(self):
        """
        Tests if there is a form created for hashing

        :var form form: Hash form template
        :var dictionary test_dict: holds test data

        :except assertion: Raised if hash form template is not found.

        :return: None
        """
        test_dict = {'text': 'hello'}
        form = HashForm(data=test_dict)
        self.assertTrue(form.is_valid())

    def test_hash_func_works(self):
        """
        Tests if the hash function works when input value is hello.

        :var tuple test: holds the values we are testing, produced by hash_to_test().
        :var string text_hash: hold result of hash function from hashlib

        :except assertion: Raised if hash_test and text_hash is not equal.

        :return: None
        """
        test = hash_to_test()
        text_hash = hashlib.sha256(test[0].encode(test[1])).hexdigest()
        self.assertEqual(test[2], text_hash)

    def test_hash_object(self):
        """
        :var tuple test: holds the values we are testing, produced by hash_to_test().
        :var Hash hash: a Hash class instant.
        :var Hash pulled_hash: A specific Hash class instant.

        :except assertion: Raised if pulled_hash Hash instant text is not the same as hash Hash instant text.

        :return: None
        """
        test = hash_to_test()
        hash = create_hash_db()
        pulled_hash = Hash.objects.get(hash=test[2])
        self.assertEqual(hash.text, pulled_hash.text)

    def test_viewing_hash(self):
        """
        Tests if you can view the hash as a response

        :var Hash hash: created database hash instant
        :var string url: holds url to be tested as a string
        :var response response: holds a self generated response

        :except assertion: Raised if the response does not contain the text in hash.text

        :return: None
        """
        hash = create_hash_db()
        url = '/hash/'+hash.hash
        response = self.create_response(url)
        self.assertContains(response, hash.text)

    def test_bad_data(self):
        """
        tests if error raises if bad information is given for hash value

        :var array test: holds array of test data.
        :var Hash hash: holds an instance of Hash.

        :except assertion: Raised if the exception 'ValidationError' is not raised.

        :return: None
        """
        def bad_hash():
            test = hash_to_test()
            hash = Hash()
            hash.hash = test[2]+'12345'
            hash.full_clean()
        self.assertRaises(ValidationError, bad_hash)

    def create_response(self, url=None):
        """
        Creates response for testing

        :param url: Url used to assign generated response.

        :return: response
        """
        return self.client.get(url)


def hash_to_test():
    """
    Easy way to create test data for hash to test.

    :var string text_test: holds test text
    :var string text_format: holds format for test text
    :var string hash_text: holds test hash

    :return: test data array that contains text, format of text, hash.
    """
    text_test = 'hello'
    text_format = 'utf-8'
    hash_test = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    element_id = 'id_text'
    return text_test, text_format, hash_test, element_id


def create_hash_db():
    """
    Creates database entry based on information supplied in hash_to_test function

    :var array test: created data array from hash_to_test
    :var Hash hash: Empty Hash instant.
    :return: Modified Hash instant
    """
    test = hash_to_test()
    hash = Hash()
    hash.text = test[0]
    hash.hash = test[2]
    hash.save()
    return hash