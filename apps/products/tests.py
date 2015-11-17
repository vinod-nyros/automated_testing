"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import unittest

from django.test import TestCase
from products.models import *
from django.test import Client


class SimpleTest(TestCase):

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class FixturesTest(TestCase):
    fixtures = ['products.yaml']

    def test_products_fixtures(self):
        p = Product.objects.get(pk=2)  # 3)
        self.assertTrue(p)


class ViewsTests(TestCase):
    fixtures = ['quickpages.yaml', 'products_all.yaml']

    def test_showroom(self):
        client = Client()
        response = client.get("/showroom/")
        self.assertEqual(response.status_code, 200)

    def test_category(self):
        client = Client()
        response = client.get("/products/general-purpose/")
        self.assertEqual(response.status_code, 200)


# @unittest.skip("These are all getting: mismatches - not sure why, the pages look fine - JJW")
class ProductConfigTests(TestCase):
    fixtures = ['quickpages.yaml', 'products_all.yaml']

    def test_choice_memory(self):
        client = Client()
        response1 = self.client.get("'/products/firewall-servers/NAT/#config'")
        response = self.client.post("/products/update_grid/",
            {'sku': ['NAT'], 'choiceid': ['1130_1,26', '1_1,22599', '5_1,7449', '3_1,30', '4_1,19663', '2_1,32411', '6_1,6587', '8_1,30', '24151_1,30', '1070_1,30', '7_1,8260', '29348_1,28984', '29351_1,28986', '18371_1,18049'], 'notes': ['']}, HTTP_REFERER='http://10.90.90.124:8000/products/firewall-servers/NAT/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn("830", response.content)

    def test_choice_pci(self):
        client = Client()
        response1 = self.client.get("'/products/firewall-servers/NAT/#config'")
        response = self.client.post("/products/update_grid/",
            {'sku': ['NAT'], 'choiceid': ['1130_1,26', '1_1,22599', '5_1,5293', '3_1,30', '4_1,19663', '2_1,32411', '6_1,22', '8_1,30', '24151_1,30', '1070_1,30', '7_1,8260', '29348_1,28984', '29351_1,28986', '18371_1,18049'], 'notes': ['']}
                , HTTP_REFERER='http://10.90.90.124:8000/products/firewall-servers/NAT/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn("1295", response.content)

    def test_choice_both(self):
        client = Client()
        response1 = self.client.get("'/products/firewall-servers/NAT/#config'")
        response = self.client.post("/products/update_grid/",
            {'sku': ['NAT'], 'choiceid': ['1130_1,26', '1_1,22599', '5_1,7449', '3_1,30', '4_1,19663', '2_1,32411', '6_1,22', '8_1,30', '24151_1,30', '1070_1,30', '7_1,8260', '29348_1,28984', '29351_1,28986', '18371_1,18049'], 'notes': ['']}
                , HTTP_REFERER='http://10.90.90.124:8000/products/firewall-servers/NAT/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertIn("1310", response.content)


class ProductsTest(TestCase):

    def setUp(self):
        categories1 = Categories.objects.create(
            name='lapi', slug='lapi', title='lapi')
        categoryimage1 = CategoryImage.objects.create(
            image='images/categories/intel-systems/corei7_75.jpeg', title='My Category', caption='My Caption', category=categories1)
        choicecategory1 = ChoiceCategory.objects.create(
            name='lapis', sohigh=2255, solow=2500)
        choice1 = Choice.objects.create(
            name='lapi', source='', price=0, cost=246.56, sortorder=222, multiplier=2, choicecategory=choicecategory1)
        option1 = Option.objects.create(
            name='laptops', usage_notes='all laptops', sortorder=222)
        product1 = Product.objects.create(
            name='mylapi', sku='mylapi', baseprice=2500.55, cost=2500.00, category=categories1, weight=20, sortorder=222) #, multiplier=2)
        productimage1 = ProductImage.objects.create(
            image='images/products/zenbook/zenbook_3.jpeg', title='lapi', caption='lapi', product=product1)
        prodopt1 = Prodopt.objects.create(
            name='mylapi', qty=1, choices_orderby='cost', product=product1, option=option1, defaultchoice=choice1)

    def test_cat_image_tag(self):
        image1 = CategoryImage.objects.get(title='My Category')
        self.assertTrue(image1.tag())

    def test_prod_image_tag(self):
        image1 = ProductImage.objects.get(title='lapi')
        self.assertTrue(image1.tag())

    def test_get_absolute_url(self):
        categories1 = Categories.objects.get(slug='lapi')
        self.assertTrue(categories1.get_absolute_url())

    def test_prods_as_divs(self):
        categories1 = Categories.objects.get(slug='lapi')
        self.assertTrue(categories1.prods_as_divs())

    def test_calc_markup(self):
        choice1 = Choice.objects.get(name='lapi')
        self.assertTrue(choice1.calc_markup)

    def test_calc_price(self):
        choice1 = Choice.objects.get(name='lapi')
        self.assertTrue(choice1.calc_price)

    def test_url(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.url)

    def test_slug(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.slug)

    def test_product_options(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.product_options())

    def test_calc_description(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.calc_description)

    def test_calc_specs(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.calc_specs)

    def test_prodopts_as_table(self):
        product1 = Product.objects.get(name='mylapi')
        self.assertTrue(product1.prodopts_as_table)

# Removed 10/14/15 JJW - Mani, can you check and make new tests for the new models, fields, and functions I added to products?
#
#    def test_as_content(self):
#        product1 = Product.objects.get(name='mylapi')
#        self.assertTrue(product1.as_content)

    def test_calc_relative_price(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        choice1 = Choice.objects.get(name='lapi')
        self.assertFalse(prodopt1.calc_relative_price(choice1))

    def test_choice_name_and_price(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        choice1 = Choice.objects.get(name='lapi')
        self.assertTrue(prodopt1.choice_name_and_price(choice1))

    def test_calc_name(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        self.assertTrue(prodopt1.calc_name)

    def test_option_choices(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        self.assertFalse(prodopt1.option_choices())

    def test_all_choices(self):
        prodopt1 = Prodopt.objects.get(name='mylapi')
        self.assertFalse(prodopt1.all_choices())
