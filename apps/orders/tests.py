"""
This is the tests file for the orders module.

Notable is the test_order test, which will run when you do:

./manage.py test orders.tests.MySeleniumTests

If you have troube debuigging, you may set 'breakpoint' to 1 near the top, which will break into an IPython shell at
the point in the code where it is referenced - see the code for usage.
"""

import time
from django.test import TestCase
from orders.models import *
from customers.models import *
from products.models import *
from datetime import datetime
from django.test import Client
from selenium import webdriver
from django.conf import settings
import selenium
from utils.tests import find_first

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
        def test_order(self):
            p = Product.objects.get(sku = 'DMZ')
            shipping_weight =p.weight
            print shipping_weight
            self.selenium.get ('%s%s' % (self.live_server_url, '/products/firewall-servers/DMZ/'))
            time.sleep(2)

            ## Now updating for new themes - JJW

            # Click an 'Add toi cart' button, update quantity
            find_first (self.selenium, '#config_summary #current a[href="#add"]','input#add_to_cart').click()
            update_qty = self.selenium.find_element_by_name('updqty')
            update_qty.send_keys('2')
            self.selenium.find_element_by_name('update').click()
            time.sleep(2)

            ## Now move to checkout page
            find_first (self.selenium, '#next a[href="/checkout/"]','#order-detail-content a[href="/checkout/"]').click()
            time.sleep(2)

            ## User Login form
            username_input = find_first(self.selenium, '#content_row input#id_identification','div#content input#id_identification')
            username_input.send_keys('test1_eracks@yopmail.com')
            password_input = find_first(self.selenium, '#content_row input#id_password','div#content input#id_password')
            password_input.send_keys('testuser1')

            find_first(self.selenium, '#content_row form input[type=submit][value=Signin]','div#content form input[type=submit][value=Signin]').click()

            ## User Info Form - should be pre-filled-in, no need
            ## Customer Info form
            organization = self.selenium.find_element_by_css_selector('table#CustomerForm input#id_organization')
            organization.send_keys('test')
            title = self.selenium.find_element_by_css_selector('table#CustomerForm input#id_title')
            title.send_keys('test')
            department = self.selenium.find_element_by_css_selector('table#CustomerForm input#id_department')
            department.send_keys('test')
            email_id = self.selenium.find_element_by_css_selector('table#CustomerForm input#id_email')
            email_id.send_keys('test1_eracks@yopmail.com')
            phone = self.selenium.find_element_by_css_selector('table#CustomerForm input#id_phone')
            phone.send_keys('+919999999999')

            ## Order Info Form
            referral_type = Select(self.selenium.find_element_by_css_selector('table#OrderForm select#id_referral_type'))
            referral_type.select_by_visible_text("Google search")
            sales_tax = Select(self.selenium.find_element_by_css_selector('table#OrderForm select#id_california_tax'))
            sales_tax.select_by_visible_text('Los Angeles')
            agree_to_terms = self.selenium.find_element_by_css_selector('table#OrderForm input#id_agree_to_terms')
            agree_to_terms.click()

            ## Shipping Address Form
            address1 = self.selenium.find_element_by_css_selector('table#AddressForm input#id_shipping-address1')
            address1.send_keys('test street, 5-4-20')
            city = self.selenium.find_element_by_css_selector('table#AddressForm input#id_shipping-city')
            city.send_keys('Los Angeles')
            state = Select(self.selenium.find_element_by_css_selector('table#AddressForm select#id_shipping-state'))
            state.select_by_visible_text('CA (California)')
            zip_code = self.selenium.find_element_by_css_selector('table#AddressForm input#id_shipping-zip')
            zip_code.send_keys('90011')

            ## Billing Address Form (use selector table#BillingAddressForm input#id_billing_name, etc)
            # if blank same as shipping, but could still test here..

            ## Payment Info Form
            payment_method1 = Select(self.selenium.find_element_by_css_selector("table#PaymentForm select#id_payment_method"))
            payment_method1.select_by_visible_text("Purchase Order")
            expiry_date1 = Select(self.selenium.find_element_by_css_selector('table#PaymentForm select#id_expiry_date_1'))
            expiry_date1.select_by_visible_text('2017')
            time.sleep(2)
            find_first(self.selenium, 'input[name=update][value=Update]','form#checkoutform div#content_row a[href="/checkout/confirm/"]').click()
            actual_shipping = self.selenium.execute_script ('''return $("#final_cart table td:contains(Shipping & Handling)+td").get(0)''')

            if breakpoint:
                from IPython import embed
                embed()

            print 'actual_shipping', type(actual_shipping), actual_shipping.text
            actual_shipping_price  = float(actual_shipping.text.strip('$'))
            expected_shipping_price = shipping_weight*2

            ## Place the order!
            find_first(self.selenium, '#content_row input[name=order][value="Place Order"]','form#confirmform a[href="/checkout/confirm/"]').click()

            if self.selenium.name == 'chrome':
                self.selenium.get_screenshot_as_file('media/test_results_screens/chrome/test_order.png')

            if self.selenium.name == 'firefox':
                self.selenium.get_screenshot_as_file('media/test_results_screens/firefox/test_order.png')

            time.sleep(5)
            self.assertEqual(expected_shipping_price, actual_shipping_price)

    class WebDriverList(list):
        def __init__(self, *drivers):
            super(WebDriverList, self).__init__(drivers)

        def quit(self):
            for driver in self:
                driver.quit()


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class FixturesTest(TestCase):
    fixtures = ['users.yaml', 'customers.yaml', 'catax.yaml', 'orders.yaml']

    def test_orders_fixtures(self):
        order1 = Order.objects.get(pk=1)
        self.assertTrue(order1)

class ViewsTests(TestCase):
    fixtures = ['users.yaml', 'customers.yaml',
                'catax.yaml', 'products.yaml', 'orders.yaml', 'quickpages.yaml']

    def test_cart(self):
        client = Client()
        response = client.get("/cart/")
        print 'this is cart'

        self.assertEqual(response.status_code, 200)
    # need to set the session with products for post request

    def test_cart_post(self):
        client = Client()
        products = Product.objects.all()
        response = client.post("/cart/", {'prod': products[0]})
        self.assertIn('cart is empty', response.content)
    # without product checkout is redircting to cart page

    def test_checkout(self):
        client = Client()
        response = client.get("/checkout/", follow=True)
        self.assertIn('Your Cart', response.content)


class ImportedOrderTest(TestCase):

    def setUp(self):
        importorder1 = ImportedOrder.objects.create(title='test@test.com', email='test@test.com', shiptype='US',
                                                    shipname='test', shiporg='test1', shipaddr1='26246 Twelve Trees Lane NW', shipcity='los angels',
                                                    shipmethod='Ground', shipcost='0', shippay='shipincl', billsame='on', iagree='on',
                                                    reftyp='repeat', paymeth='byccard', orderstatus='open', ordernum='54364')

    def test_name(self):
        importedorder1 = ImportedOrder.objects.get(title='test@test.com')
        shipname1 = importedorder1.shipname
        name1 = importedorder1.name()
        self.assertEqual(shipname1, name1)

    def test_org(self):
        importedorder1 = ImportedOrder.objects.get(title='test@test.com')
        shiporg1 = importedorder1.shiporg
        org1 = importedorder1.org()
        self.assertEqual(shiporg1, org1)

    def test_name_org(self):
        importedorder1 = ImportedOrder.objects.get(title='test@test.com')
        name_org1 = importedorder1.name_org()
        self.assertTrue(name_org1)


class OrderPaymentTest(TestCase):

    def setUp(self):
        ex_date = datetime(2015, 12, 31, 18, 23, 29, 227)
        user2 = User.objects.create(
            username="testuser2", email="testuser2@yahoo.com", password="testuser2")
        customer2 = Customer.objects.get(user=user2)
        address2 = Address.objects.create(customer=customer2, address2='street', city='texas', state='CA',
                                          zip='556655', country='US', phone='123456', email='testuser2@yahoo.com', type='shipping')
        order1 = Order.objects.create(customer=customer2, shipping=40.00, shipping_method='ground', preferred_shipper='Any',
                                      referral_type='google', ship_to_address=address2, bill_to_address=address2, status='website', source='website')
        orderpayment1 = OrderPayment.objects.create(
            order=order1, payment_method='byccard', expiry_date=ex_date, user=user2)

    def test_expiry_mmyy(self):
        user2 = User.objects.get(email='testuser2@yahoo.com')
        customer2 = Customer.objects.get(user=user2)
        order1 = Order.objects.get(customer=customer2)
        orderpayment1 = OrderPayment.objects.get(order=order1)
        print orderpayment1
        print orderpayment1.expiry_mmyy()



