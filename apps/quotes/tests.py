"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from quotes.models import *


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
