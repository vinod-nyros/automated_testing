from django.core.management.base import NoArgsCommand
import unittest
import random
import string
import time
from django.contrib.auth.models import User, Group
from home.models import *
from django.test import TestCase
from django.test import Client
from selenium import webdriver
from django.conf import settings
from customers.models import *
from products.models import *
from utils.tests import find_first
#from selenium.webdriver.common.action_chains import ActionChains


timeout = 5

class Command(NoArgsCommand):
    help = """
    Run the test cases to loop through the products and select the choices other than default'
    """

    def handle_noargs(self, **options):
        suite = unittest.TestLoader().loadTestsFromTestCase(MySeleniumTests)
        unittest.TextTestRunner().run(suite)

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
        # fixtures = ['catax.yaml', 'products.yaml', 'obdjects.yaml']
        csrf_client = Client(enforce_csrf_checks=True)

        def setUp(self):
            pass
            # user1 = User.objects.create_user(
            #     username="test1_eracks@yopmail.com", email="test1_eracks@yopmail.com", password="testuser1")

        @classmethod
        def setUpClass(cls):
            # cls.selenium = driver
            cls.drivers = WebDriverList(webdriver.Firefox())
            super(MySeleniumTests, cls).setUpClass()

        @classmethod
        def tearDownClass(cls):
            # cls.selenium.quit()
            cls.drivers.quit()
            super(MySeleniumTests, cls).tearDownClass()

        # @unittest.skip("This is getting: a 302 instead of 200 - SSL issue?")
        @test_drivers()
        def test_choices(self):
            ## start with NAT model, jump to configurator (or tab, in Legacy)
            self.selenium.get('https://eracks.com/products/firewall-servers/NAT/#config')
            time.sleep(timeout)

            ## Get prices
            base_price = self.selenium.find_element_by_css_selector ('#config_summary #current .baseprice b').text
            price_before = self.selenium.find_element_by_css_selector ('#config_summary #current .price b').text
            print "***"*20
            print base_price
            print price_before
            print "***"*20
            if base_price == price_before:
                print "need to change options"
            else:
                print "choices have changed"

            # Mani: the below index-based css selectors are not working now -
            # please always use meaningful selectors that are based on the actual option and choice, such as:
            # this, which I tested in the firefox console and works:
            # $('td.3_1.dropdowns > select.choiceid > option[value="3_1,9"]')
            #
            # Even something like:
            # self.selenium.find_element_by_css_selector('select.choiceid > option[value="3_1,9"]')
            # Should work - let me know,
            # Joe

            # Joe:  I tried this before only and yes it is working in firefox console but not working
            # with selenium

            # I tried in many ways like below code, but every time it is giving
            # InvalidSelectorError: An invalid or illegal selector was specified
            # so I wrote the code which was commented by you. but that code is working fine
            # -Mani
            self.selenium.find_element_by_css_selector(
              'select.choiceid option[value="1130_1,27"]').click()
              #'option:contains("LOCK: 1U lockable chassis, 300WPS 25.75"D ($35.00)")').click()

            #LOCK: 1U lockable chassis, 300WPS 25.75"D ($35.00)

            # time.sleep(timeout)


            self.selenium.find_element_by_css_selector(
               'select.choiceid option[value="1_1,17418"]').click()
            print "&&&&"*10
            time.sleep(timeout)
            self.selenium.find_element_by_css_selector(
               'select.choiceid option[value="5_1,7449"]').click()
            self.selenium.find_element_by_css_selector(
               'select.choiceid option[value="3_1,36425"]').click()
            time.sleep(timeout)

            ## re-get and check price
            price_after = self.selenium.find_element_by_css_selector ('#config_summary #current .price b').text
            print price_after
            self.assertNotEqual(price_after, price_before)

        # @test_drivers()
        # def test_products(self):
        #     import time

        #     self.selenium.get(
        #         'https://eracks.com/')

        #     time.sleep(timeout)

        #     element_to_hover = self.selenium.find_element_by_css_selector(
        #        'div#product_list ul.nav-bar.vertical li.has-flyout a.flyout-toggle')
        #     hover = ActionChains(self.selenium).move_to_element(element_to_hover)
        #     hover.perform()
        #     time.sleep(timeout)
        #     self.selenium.find_element_by_css_selector(
        #        'div#product_list ul.nav-bar.vertical li.has-flyout div.flyout.small div.product a:nth-child(1)').click()
        #     time.sleep(timeout)

            # price_after = self.selenium.find_element_by_css_selector(
            #     'div#current div.price b').text
            # self.assertNotEqual(
            #     price_after, price_before)


    class WebDriverList(list):
        def __init__(self, *drivers):
            super(WebDriverList, self).__init__(drivers)

        def quit(self):
            for driver in self:
                driver.quit()
