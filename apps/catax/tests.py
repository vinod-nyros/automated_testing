"""
Test test for Selenium - JJW - attempt to do :contains with js - run with:

./manage.py test catax.tests
./manage.py test catax.tests.MySeleniumTests.test_login

SOLVED: with ipython embed - very useful!

The 'embed()' call, below, breaks into a shell at that point!

Set 'breakpoint' to 1 to try it - JJW

Don't forget to turn it back off before checking in, oth4erwise tests will fail for trhe next guy
(Such as CI, CircleCI, etc)

See also my IPython command line history, at the bottom..
"""

import time  #, sys

from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from utils.tests import find_first

breakpoint = 0


class MySeleniumTests(LiveServerTestCase):
    fixtures = ['user-data.json', 'home.yaml']

    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()

    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))   # '/accounts/signin/'))

        if breakpoint:
          from IPython import embed
          embed()  # breaks into an ipython shell here!
        else:
          return

        #time.sleep (5)
        #username_input = self.selenium.find_element_by_name("identification")  # there are 2! so use css..

        #self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signin/'))
        ## get the visible one, not the hidden dialog
        #username_input = find_first (self.selenium, "#content_row input[name=identification]", "#content input[name=identification]")


        print 'USERNAME_INPUT', username_input

        # old stuff from Django example:
        username_input.send_keys('myuser')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('secret')
        self.selenium.find_element_by_xpath('//input[@value="Signin"]').click()
        #time.sleep (15)


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


my_ipython_commandline_history='''

In [42]: %hist
username_input
username_input.id
username_input.is_displayed
username_input.is_displayed()
username_input.text
username_input.tag_name
username_input
username_input.get_attribute ('type')
username_input.get_attribute ('id')
username_input.get_attribute ('name')
username_input.get_attribute ('value')
username_input.get_attribute ('class')
username_input.click()
username_input.find_elements_by_css_selector ('input')
self.selenium.find_elements_by_css_selector ('input')
self.selenium.find_elements_by_css_selector ('input[name]')
self.selenium.find_elements_by_css_selector ('input[name=identification]')
self.selenium.find_elements_by_css_selector ('#content_row input[name=identification]')
self.selenium.execute_script ('$("#content_row input[name=identification]")')
e = self.selenium.execute_script ('$("#content_row input[name=identification]")')
e
print e
e = self.selenium.execute_script ('return $("#content_row input[name=identification]")')
e
e.items()
print type(e)
e.keys()
e['text']
e['text']()
e = self.selenium.execute_script ('return $("#content_row input[name=identification]").get(0)')
e
e.text
e.send_keys('joe')
e = self.selenium.execute_script ('return $("table tr td h5:contains(' + 'eRacks Bus' + ')").get(0)')
e
e.text
e = self.selenium.execute_script ('return $("table tr td h5:contains(' + 'eRacks Bus' + ')+div").get(0)')
e
e.text
e.tag_name

'''
