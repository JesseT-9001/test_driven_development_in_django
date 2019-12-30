"""
The module was used as an example of a functional test using selenium.
"""

from selenium import webdriver


def func_test() -> None:
    """
    :var webdriver safari: Used to operate the safari web-browser
    :var string localhost_8000: Holds the localhost url with port number
    :var string test_text: Hold what string you would like tested
    :except assertion: Raised if test_text is not in the page source
    :return: nothing
    """
    safari = webdriver.Safari()
    localhost_8000 = 'http://localhost:8000'
    safari.get(localhost_8000)

    test_text = 'install'
    assert test_text in safari.page_source
    safari.close()
