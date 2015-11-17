"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from quotes.models import *
from django.conf import settings
from selenium import webdriver
from django.test import Client
from utils.tests import find_first
import time
from products.views import send_quote_email

class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}


class FixturesTest(TestCase):
    fixtures = ['users.yaml', 'customers.yaml', 'quotes.yaml']

    def test_customers_fixtures(self):
        quote1 = Quote.objects.get(pk=55143)
        self.assertTrue(quote1)


class QuoteTest(TestCase):

    def setUp(self):
        user2 = User.objects.create(
            username="testuser2", email="testuser2@yahoo.com", password="testuser2")
        customer2 = Customer.objects.get(user=user2)
        quote1 = Quote.objects.create(customer=customer2, quote_number='022222-LAPI', approved_by=user2, valid_for=10,
                                      purchase_order='2222-P-00-260563', customer_reference='Laptop  note, 48 coress', terms='ccard', shipping=222, target=22222)
        quotelineitem1 = QuoteLineItem.objects.create(
            quote=quote1, model='lapi222', quantity=22, description='descriptiondescription', cost=2222.22, price=2222)

    def test_is_template(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        self.assertFalse(quote1.is_template())

    def test_totprice(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        for q in quote1.quotelineitem_set.all():
            total_price = q.price*q.quantity
        self.assertEqual(quote1.totprice, total_price)

    def test_totqty(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        self.assertEqual(quote1.totqty, 22)

    def test_summary(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        self.assertTrue(quote1.summary)

    def test_header_items(self):
        quote1 = Quote.objects.get(quote_number='022222-LAPI')
        self.assertTrue(quote1.header_items)


breakpoint = 0

driver = None

if settings.SELENIUM_DRIVER=='Firefox':
    if settings.FIREFOXPRESENT:
        driver = True #webdriver.Firefox()
elif settings.SELENIUM_DRIVER=='Chrome':
    if settings.CHROMEPRESENT:
        driver = webdriver.Chrome(executable_path=settings.CHROME_DRIVER_PATH)

if driver:
    from django.test import LiveServerTestCase
    # changed in django 1.7 to load staticfiles
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase
    # from selenium.webdriver.firefox.webdriver import WebDriver
    from selenium.webdriver.support.select import Select
    import functools
    def test_drivers(driver_pool='drivers'):
        def wrapped(test_func):
            @functools.wraps(test_func)
            def decorated(test_case, *args, **kwargs):
                test_class = test_case.__class__
                web_driver_pool = getattr(test_class, driver_pool)
                for web_driver in web_driver_pool:
                    setattr(test_case, 'selenium', web_driver)
                    test_func(test_case, *args, **kwargs)
            return decorated
        return wrapped

    class MySeleniumTests(StaticLiveServerTestCase):
        selenium = None
        fixtures = ['catax.yaml', 'products.yaml', 'quickpages.yaml']
        csrf_client = Client(enforce_csrf_checks=True)

        def setUp(self):
            user1 = User.objects.create_user(
                username="test1_eracks@yopmail.com", email="test1_eracks@yopmail.com", password="testuser1")

        @classmethod
        def setUpClass(cls):
            cls.drivers = WebDriverList(webdriver.Firefox())
            super(MySeleniumTests, cls).setUpClass()

        @classmethod
        def tearDownClass(cls):
            cls.drivers.quit()
            super(MySeleniumTests, cls).tearDownClass()

        @test_drivers()
        def login_with_email(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

            ## Select the visible ones, not the modal(hidden) one - fill in user & pw, submit
            username_input = find_first (self.selenium, '#content_row input#id_identification', '#content input#id_identification')
            username_input.send_keys('test1_eracks@yopmail.com')
            password_input = find_first (self.selenium, '#content_row input#id_password', '#content input#id_password')
            password_input.send_keys('testuser1')
            find_first (self.selenium, '#content_row input[type=submit][value=Signin]', '#content input[type=submit][value=Signin]').click()
            time.sleep(2)
            self.selenium.get('%s%s' % (self.live_server_url, '/products/firewall-servers/DMZ/'))
            time.sleep(5)
            click_getquote = self.selenium.find_element_by_id('get_quote').click()
            email = 
            getquote_with_email = self.selenium.find_element_by_id('get_quote').click()
            time.sleep(200)

            
            ## grab screens
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_login.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_login.png')
            self.assertIn("Your quote request has been sent", self.selenium.page_source)
            

    class WebDriverList(list):
        def __init__(self, *drivers):
            super(WebDriverList, self).__init__(drivers)

        def quit(self):
            for driver in self:
                driver.quit()
