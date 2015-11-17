import unittest
import time
import urllib
import os.path

from django.conf import settings
from django.test import TestCase
from django.test import Client
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User, Group
from home.models import *
from utils.tests import find_first

from selenium import webdriver
from htmlvalidator.client import ValidatingClient
from xml.dom import minidom


driver = None

if settings.SELENIUM_DRIVER=='Firefox':
    if settings.FIREFOXPRESENT:
        driver = True   #webdriver.Firefox()
elif settings.SELENIUM_DRIVER=='Chrome':
    if settings.CHROMEPRESENT:
        driver = webdriver.Chrome(executable_path=settings.CHROME_DRIVER_PATH)

if driver:
    from django.test import LiveServerTestCase
    # changed in django 1.7 to load staticfiles
    from django.contrib.staticfiles.testing import StaticLiveServerTestCase
    #from selenium import webdriver
    # from selenium.webdriver.firefox.webdriver import WebDriver
    from selenium.webdriver.common.keys import Keys
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

    if settings.USEVIRTUALDISPLAY:
        # not needed, I don't think, it's in pyvirtualdisplay:
        #from xvfbwrapper import Xvfb

        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(1366, 768))
        display.start()
        #display.stop()


    # In-browser tests - only performed if Firefox is present

    class SeleniumTestCase(LiveServerTestCase):
        selenium = None
        fixtures = ['quickpages.yaml','products_all.yaml','users.yaml','bloglets.yaml']

        def setUp(self):
            user1 = User.objects.create_user(
                username="testmailname1@yopmail.com", email="testmailname1@yopmail.com", password="testuser1")

        @classmethod
        def setUpClass(cls):
            #cls.xvfb = Xvfb(width=1280, height=720)
            # cls.xvfb.start()
            #cls.drivers = WebDriverList(webdriver.Chrome(executable_path=settings.CHROME_DRIVER_PATH),webdriver.Firefox())
            cls.drivers = WebDriverList(webdriver.Firefox())
            super(SeleniumTestCase, cls).setUpClass()

        @classmethod
        def tearDownClass(cls):
            # JJW - why does this fault?: cls.wd.quit()
            cls.drivers.quit()
            super(SeleniumTestCase, cls).tearDownClass()
            # cls.xvfb.stop()
        @test_drivers()
        def test_contact(self):
            #display = Display(visible=0, size=(800, 600))
            # display.start()

            # now Firefox will run in a virtual display.
            # you will not see the browser.
            browser = self.drivers  # webdriver.Firefox()
            print "**" * 50
            print "opening the site"
            print self.selenium.name
            print "**" * 50
            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

            username_input = find_first (self.selenium,
                    '#content_row form fieldset input#id_identification',
                    '#content form fieldset input#id_identification'
                  )
            #username_input = self.selenium.find_element_by_css_selector(
                #'#content_row form fieldset input#id_identification')
                #'.seven.columns>form>fieldset>p>input#id_identification')
            username_input.send_keys('testmailname1@yopmail.com')

            password_input = find_first (self.selenium,
                  '#content_row form fieldset input#id_password',
                  '#content form fieldset input#id_password'
                )
            #password_input = self.selenium.find_element_by_css_selector(
                #'#content_row form fieldset input#id_password')
                #'.seven.columns>form>fieldset>p>input#id_password')
            password_input.send_keys('testuser1')

            find_first (self.selenium,
                  '#content_row form input[type=submit][value=Signin]',
                  '#content form input[type=submit][value=Signin]'
                ).click()
            #self.selenium.find_element_by_css_selector(
                #'#content_row form input[type=submit][value=Signin]').click()
                #'.seven.columns>form>input').click()
            time.sleep(3)
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_contact.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_contact.png')
            time.sleep(3)
            self.assertIn("You have been signed in", self.selenium.page_source)
            time.sleep(3)
            # self.selenium.quit()
            print "**" * 50
            print "closing the site"
            print "**" * 50
            # display.stop()

    class WebDriverList(list):
        def __init__(self, *drivers):
            super(WebDriverList, self).__init__(drivers)

        def quit(self):
            for driver in self:
                driver.quit()

    class MySeleniumTests(StaticLiveServerTestCase):
        selenium = None
        fixtures = ['quickpages.yaml','users.yaml','bloglets.yaml', 'products_all.yaml', 'home.yaml']
        csrf_client = Client(enforce_csrf_checks=True)
        #fixtures = ['user-data.json']

        def setUp(self):
            user1 = User.objects.create_user(
                username="test1_eracks@yopmail.com", email="test1_eracks@yopmail.com", password="testuser1")
            my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'myuser')

        @classmethod
        def setUpClass(cls):
            #cls.drivers = WebDriverList(webdriver.Chrome(executable_path=settings.CHROME_DRIVER_PATH),webdriver.Firefox())
            cls.drivers = WebDriverList(webdriver.Firefox())
            #cls.selenium = webdriver.Firefox()  #driver
            super(MySeleniumTests, cls).setUpClass()

        @classmethod
        def tearDownClass(cls):
            # cls.selenium.quit()
            cls.drivers.quit()
            super(MySeleniumTests, cls).tearDownClass()
        from django.test.utils import override_settings

        @test_drivers()
        def test_login(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))

            ## Select the visible ones, not the modal(hidden) one - fill in user & pw, submit
            username_input = find_first (self.selenium, '#content_row input#id_identification', '#content input#id_identification')
            username_input.send_keys('test1_eracks@yopmail.com')
            password_input = find_first (self.selenium, '#content_row input#id_password', '#content input#id_password')
            password_input.send_keys('testuser1')
            find_first (self.selenium, '#content_row input[type=submit][value=Signin]', '#content input[type=submit][value=Signin]').click()
            time.sleep(5)

            ## grab screens
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_login.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_login.png')
            self.assertIn("You have been signed in", self.selenium.page_source)

        @test_drivers()
        #@override_settings(DEBUG=True)
        def test_signindialog(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/'))
            time.sleep(5)

            ## Make popup visible by clicking Login
            find_first (self.selenium, "#header_right ul li:first-child a", 'a#show-login-dialog').click()
            time.sleep(5)

            ## Enter username & email
            username_input = self.selenium.find_element_by_id('id_identification')
            username_input.send_keys('test1_eracks@yopmail.com')
            password_input = self.selenium.find_element_by_css_selector('input#id_password')
            password_input.send_keys('testuser1')

            ## Submit the form, grab screens
            find_first (self.selenium, '#signinTab form input[value=Signin]', '#signin form input[value=Signin]').click()
            time.sleep(5)
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_signindialog.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_signindialog.png')
            self.assertIn("You have been signed in", self.selenium.page_source)

        @test_drivers()
        def test_signupdialog(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/'))
            time.sleep(5)

            ## Make popup visible by clicking Login
            find_first (self.selenium, "#header_right ul li:first-child a", "a#show-login-dialog").click()
            time.sleep(5)

            # click Signup tab, enter username & email
            self.selenium.find_element_by_css_selector('#signin_signup_modal a[href="#signup"]').click()
            username = self.selenium.find_element_by_id('id_username')
            if self.selenium.name=='chrome':
                username.send_keys('test114c_eracks')
            if self.selenium.name=='firefox':
                username.send_keys('test114f_eracks')
            email = self.selenium.find_element_by_id(
                'id_email')
            if self.selenium.name=='chrome':
                email.send_keys('test114c_eracks@yopmail.com')
            if self.selenium.name=='firefox':
                email.send_keys('test114f_eracks@yopmail.com')
            time.sleep(5)

            # Submit the form
            find_first (self.selenium, '#signupTab form input[value=Signup]', '#signup form input[value=Signup]').click()
            time.sleep(5)

            ## Save screenshots
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_signupdialog.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_signupdialog.png')
            self.assertIn('Thank', self.selenium.page_source)

        @test_drivers()
        def test_signup_username(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signup/'))

            ## Fill in username
            username = find_first (self.selenium, '#content_row input#id_username','#content input#id_username')
            if self.selenium.name=='chrome':
                username.send_keys('test113c_eracks')
            if self.selenium.name=='firefox':
                username.send_keys('test113f_eracks')

            ## Fill in email
            email = find_first (self.selenium, '#content_row input#id_email', '#content input#id_email')
            if self.selenium.name=='chrome':
                email.send_keys('test113c_eracks@yopmail.com')
            if self.selenium.name=='firefox':
                email.send_keys('test113f_eracks@yopmail.com')

            # Submit form, save screen grabs
            find_first (self.selenium, '#content_row input[type=submit][value=Signup]', '#content input[type=submit][value=Signup]').click()
            time.sleep(5)
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_signup_username.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_signup_username.png')
            self.assertIn('Thank', self.selenium.page_source)

        @test_drivers()
        def test_signup_email(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/accounts/signup/'))

            ## Fill in username
            username = find_first (self.selenium, '#content_row input#id_username', '#content input#id_username')
            if self.selenium.name=='chrome':
                username.send_keys('test112c_eracks@yopmail.com')
            if self.selenium.name=='firefox':
                username.send_keys('test112f_eracks@yopmail.com')

            ## Fill in email
            email = find_first (self.selenium, '#content_row input#id_email', '#content input#id_email')
            if self.selenium.name=='chrome':
                email.send_keys('test112c_eracks@yopmail.com')
            if self.selenium.name=='firefox':
                email.send_keys('test112f_eracks@yopmail.com')

            ## submit form, grab screens
            find_first (self.selenium, '#content_row input[type=submit][value=Signup]', '#content input[type=submit][value=Signup]').click()
            time.sleep(5)
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_signup_email.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_signup_email.png')
            self.assertIn('Thank', self.selenium.page_source)

        @test_drivers()
        def test_contact(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/contact/'))
            name = self.selenium.find_element_by_id("id_name")
            name.clear()
            name.send_keys("name1")

            email = find_first (self.selenium, '#content_row input#id_email', '#content input#id_email')
            email.clear()
            email.send_keys("testmailname1@yopmail.com")

            desc = self.selenium.find_element_by_id("id_description")
            desc.clear()
            desc.send_keys("sample description")

            body = self.selenium.find_element_by_id("id_body")
            body.clear()
            body.send_keys("sample body")

            # self.selenium.find_element_by_id("contact").click()

            submit = self.selenium.find_element_by_id("contact")
            import time
            #time.sleep(2)
            submit.send_keys(Keys.RETURN)
            #time.sleep(5)
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/testcontact.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/testcontact.png')
            self.assertIn("Thank you", self.selenium.page_source)

        @test_drivers()
        def test_contact_long_email(self):
            self.selenium.get('%s%s' % (self.live_server_url, '/contact/'))
            name = self.selenium.find_element_by_id("id_name")
            name.clear()
            name.send_keys("lengthen email")

            email = find_first (self.selenium, '#content_row input#id_email', '#content input#id_email')
            email.clear()
            email.send_keys("lengthentestindevwithverylargeemailid@yopmail.com")

            desc = self.selenium.find_element_by_id("id_description")
            desc.clear()
            desc.send_keys("lengthen test with very large email")

            body = self.selenium.find_element_by_id("id_body")
            body.clear()
            body.send_keys("lengthen test with very large email")

            # self.selenium.find_element_by_id("contact").click()

            submit = self.selenium.find_element_by_id("contact")
            time.sleep(2)
            submit.send_keys(Keys.RETURN)
            #time.sleep(5)
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_contact_long_email.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_contact_long_email.png')
            self.assertIn("Thank you", self.selenium.page_source)

        @test_drivers()
        def test_admin_login(self):
            self.selenium.get(
                '%s%s' % (self.live_server_url, '/admin/login/'))
            username_input = self.selenium.find_element_by_css_selector(
                'input#id_username')
            username_input.send_keys('myuser')
            password_input = self.selenium.find_element_by_css_selector(
                'input#id_password')
            password_input.send_keys('myuser')
            self.selenium.find_element_by_css_selector(
                'input.grp-button.grp-default').click()
            import time
            #time.sleep(5)
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_admin_login.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_admin_login.png')
            self.assertIn("Authentication and Authorization", self.selenium.page_source)

        @test_drivers()
        def test_admin_featuredimage(self):
            self.selenium.get(
                '%s%s' % (self.live_server_url, '/admin/home/featuredimage/'))
            username_input = self.selenium.find_element_by_css_selector(
                'input#id_username')
            username_input.send_keys('myuser')
            password_input = self.selenium.find_element_by_css_selector(
                'input#id_password')
            password_input.send_keys('myuser')
            self.selenium.find_element_by_css_selector(
                'input.grp-button.grp-default').click()
            import time
            #time.sleep(5)
            if self.selenium.name=='chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_admin_featuredimage.png')
            if self.selenium.name=='firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_admin_featuredimage.png')
            self.assertIn("Featured images", self.selenium.page_source)


# Unit tests

class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ViewsTests(TestCase):
    fixtures = ['quickpages.yaml']

    def setUp(self):
        user1 = User.objects.create_user(
            username="testmailname1", email="testmailname1@yopmail.com", password="testuser1")

    def test_contact(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_contact_post(self):
        client = Client()
        response = client.post(
            "/contact/", {'name': 'test', 'email': 'test@yopmail.com', 'topic': 'Network design services', 'description': 'test', 'body': 'test'})
        self.assertIn("Thank you", response.content)

    def test_user_signup(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_user_signup_post(self):
        client = Client()
        response = client.post(
            "/accounts/signup/", {'username': 'sometestuser', 'email': 'sometestuser@yopmail.com'})
        self.assertIn("Thank you", response.content)

    def test_user_login(self):
        client = Client()
        response = client.post(
            "/accounts/login/", {'identification': 'testmailname1', 'password': 'testuser1'}, follow=True)
        self.assertIn("You have been signed in", response.content)
        # self.assertEqual(response.status_code, 200)


class FixturesTest(TestCase):
    fixtures = ['home.yaml']

    def test_home_fixtures(self):
        fimage1 = FeaturedImage.objects.get(pk=53684)
        all_f_imgs = FeaturedImage.objects.all()
        self.assertTrue(fimage1)


class FeaturedImageTest(TestCase):

    def setUp(self):
        FeaturedImage.objects.create(
            image='images/slideshow/NAS72_frontpage.jpg', link='/testimage/', title='testimage', caption='testimage')

    def test_as_img(self):
        featuredimage1 = FeaturedImage.objects.get(title='testimage')
        print featuredimage1.as_img()
        self.assertTrue(featuredimage1.as_img())

    def test_as_caption(self):
        featuredimage1 = FeaturedImage.objects.get(title='testimage')
        print featuredimage1.as_caption()
        self.assertTrue(featuredimage1.as_caption())

    def test_as_content(self):
        featuredimage1 = FeaturedImage.objects.get(title='testimage')
        print featuredimage1.as_content()
        self.assertTrue(featuredimage1.as_content())

# SSL issue?:
# @unittest.skip("These are all getting: UnicodeEncodeError: 'ascii' codec can't encode character u'\u201c' in position 31: ordinal not in range(128)")
# I am not getting any error when running this error
class HtmlValidation(TestCase):

    fixtures = ['products.yaml', 'quickpages.yaml', 'home.yaml']

    def setUp(self):
        self.client = ValidatingClient()

    def test_main_page(self):
        response = self.client.get("https://eracks.com/")
        self.assertEqual(response.status_code, 200)

    def test_services_page(self):
        response = self.client.get("https://eracks.com/services/")
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get("https://eracks.com/contact/")
        self.assertEqual(response.status_code, 200)

    def test_customers_page(self):
        response = self.client.get("https://eracks.com/customers/")
        self.assertEqual(response.status_code, 200)

    def test_cart_page(self):
        response = self.client.get("https://eracks.com/cart/")
        self.assertEqual(response.status_code, 200)

    def test_showroom_page(self):
        response = self.client.get("https://eracks.com/showroom/")
        self.assertEqual(response.status_code, 200)

    def test_partners_page(self):
        response = self.client.get("https://eracks.com/partners/")
        self.assertEqual(response.status_code, 200)

    def test_press_page(self):
        response = self.client.get("https://dev.eracks.com/press/")
        self.assertEqual(response.status_code, 200)

    def test_corporate_page(self):
       response = self.client.get("https://dev.eracks.com/corporate/")
       self.assertEqual(response.status_code, 200)

    #def test_product_premium(self):
    #    response = self.client.get("https://dev.eracks.com/products/general-purpose/PREMIUM/")
    #    self.assertEqual(response.status_code, 200)

    def test_product_dmz(self):
        response = self.client.get("https://dev.eracks.com/products/firewall-servers/DMZ/")
        self.assertEqual(response.status_code, 200)


class CheckFilesTest(TestCase):

    def test_robots(self):
        """
        Tests wether robots file exists or not
        """
        self.assertTrue(os.path.exists('static/robots.txt'))

    def test_humans(self):
        """
        Tests wether humans file exists or not
        """
        self.assertTrue(os.path.exists('static/humans.txt'))

    def test_ror(self):
        """
        Tests wether ror file exists or not
        """
        self.assertTrue(os.path.exists('static/ror.xml'))

    def test_sitemapxml(self):
        """
        Tests wether sitemap file exists or not
        """
        self.assertTrue(os.path.exists('static/sitemap.xml'))

    def test_sitemaphtml(self):
        """
        Tests wether sitemap html file exists or not
        """
        self.assertTrue(os.path.exists('static/sitemap.html'))

    def test_favicon(self):
        response = self.client.get("/favicon.ico/")
        self.assertEqual(response.status_code, 200)


# SSL issue?:
# @unittest.skip("This is getting: a 302 instead of 200 - SSL issue?")
class AdminLinksTest(TestCase):

    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'myuser')
        self.client.login(username="myuser",password="myuser")

    def test_admin(self):
        """
        Tests wether can we loggin to admin panel or not
        """
        response = self.client.get("/admin/")
        self.assertIn("Authentication and Authorization",response.content)
    def test_admin_user(self):
        """
        Tests admin/auth/user url in admin panel
        """
        response = self.client.get("/admin/auth/user/")
        self.assertIn("Users",response.content)
    def test_admin_group(self):
        """
        Tests admin/auth/group url in admin panel
        """
        response = self.client.get("/admin/auth/group/")
        self.assertIn("Groups",response.content)
    def test_admin_redirects(self):
        """
        Tests admin/redirects url in admin panel
        """
        response = self.client.get("/admin/redirects/")
        self.assertIn("Redirects",response.content)
    def test_admin_sites(self):
        """
        Tests admin/sites/site/ url in admin panel
        """
        response = self.client.get("/admin/sites/site/")
        self.assertIn("Sites",response.content)
    def test_admin_featuredimage(self):
        """
        Tests admin/home/featuredimage url in admin panel
        """
        response = self.client.get("/admin/home/featuredimage/")
        self.assertIn("Featured images",response.content)
    def test_admin_category(self):
        """
        Tests admin/bloglets/category/ url in admin panel
        """
        response = self.client.get("/admin/bloglets/category/")
        self.assertIn("Categories",response.content)
    def test_admin_post(self):
        """
        Tests admin/bloglets/post/ url in admin panel
        """
        response = self.client.get("/admin/bloglets/post/")
        self.assertIn("Posts",response.content)
    def test_admin_quickpage(self):
        """
        Tests admin/quickpages/quickpage/ url in admin panel
        """
        response = self.client.get("/admin/quickpages/quickpage/")
        self.assertIn("Quick pages",response.content)
    def test_admin_quicksnippet(self):
        """
        Tests admin/quickpages/quicksnippet/ url in admin panel
        """
        response = self.client.get("/admin/quickpages/quicksnippet/")
        self.assertIn("Quick snippets",response.content)
    def test_admin_customerimage(self):
        """
        Tests admin/customers/customerimage/ url in admin panel
        """
        response = self.client.get("/admin/customers/customerimage/")
        self.assertIn("Customer images",response.content)
    def test_admin_customer(self):
        """
        Tests admin/customers/customer/ url in admin panel
        """
        response = self.client.get("/admin/customers/customer/")
        self.assertIn("Customers",response.content)
    def test_admin_testimonial(self):
        """
        Tests admin/customers/testimonial/ url in admin panel
        """
        response = self.client.get("/admin/customers/testimonial/")
        self.assertIn("Testimonials",response.content)
    def test_admin_importedorder(self):
        """
        Tests admin/orders/importedorder/ url in admin panel
        """
        response = self.client.get("/admin/orders/importedorder/")
        self.assertIn("Imported orders",response.content)
    def test_admin_order(self):
        """
        Tests admin/orders/order/ url in admin panel
        """
        response = self.client.get("/admin/orders/order/")
        self.assertIn("Orders",response.content)
    def test_admin_categories(self):
        """
        Tests admin/products/categories/ url in admin panel
        """
        response = self.client.get("/admin/products/categories/")
        self.assertIn("Categories",response.content)
    def test_admin_choicecategory(self):
        """
        Tests admin/products/choicecategory/ url in admin panel
        """
        response = self.client.get("/admin/products/choicecategory/")
        self.assertIn("choicecategory",response.content)
    def test_admin_prodopt(self):
        """
        Tests admin/products/prodopt/ url in admin panel
        """
        response = self.client.get("/admin/products/prodopt/")
        self.assertEqual(response.status_code, 200)
    def test_admin_choice(self):
        """
        Tests admin/products/choice/ url in admin panel
        """
        response = self.client.get("/admin/products/choice/")
        self.assertIn("choices",response.content)
    def test_admin_option(self):
        """
        Tests admin/products/option/ url in admin panel
        """
        response = self.client.get("/admin/products/option/")
        self.assertIn("Options",response.content)
    def test_admin_product(self):
        """
        Tests admin/products/product/ url in admin panel
        """
        response = self.client.get("/admin/products/product/")
        self.assertIn("Products",response.content)
    def test_admin_catax(self):
        """
        Tests admin/catax/catax/ url in admin panel
        """
        response = self.client.get("/admin/catax/catax/")
        self.assertIn("CA Taxes",response.content)
    def test_admin_quote(self):
        """
        Tests admin/quotes/quote/ url in admin panel
        """
        response = self.client.get("/admin/quotes/quote/")
        self.assertIn("Quotes",response.content)
    def test_admin_sql(self):
        """
        Tests admin/sqls/sql/ url in admin panel
        """
        response = self.client.get("/admin/sqls/sql/")
        self.assertIn("Sqls",response.content)
    def test_admin_scripts(self):
        """
        Tests admin/webshell/script/ url in admin panel
        """
        response = self.client.get("/admin/webshell/script/")
        self.assertEqual(response.status_code, 200)
    def test_admin_address(self):
        """
        Tests admin/email_extras/address/ url in admin panel
        """
        response = self.client.get("/admin/email_extras/address/")
        self.assertIn("Addresses",response.content)
    def test_admin_keys(self):
        """
        Tests admin/email_extras/key/ url in admin panel
        """
        response = self.client.get("/admin/email_extras/key/")
        self.assertIn("Keys",response.content)
    def test_admin_tag(self):
        """
        Tests admin/taggit/tag/ url in admin panel
        """
        response = self.client.get("/admin/taggit/tag/")
        self.assertIn("Tags",response.content)



class SitemapLinksTest(TestCase):
    def test_all_links(self):
        doc = minidom.parse("static/sitemap.xml")
        all_links = doc.getElementsByTagName("loc")
        for link in all_links:
            print "###"*30
            print link.firstChild.data
            time.sleep(1)
            response = urllib.urlopen(link.firstChild.data)
            if response.getcode() != 200:
              print 'sitemap incorrect:', link.firstChild.data
            self.assertEqual(response.getcode(), 200)
            print "###"*30
