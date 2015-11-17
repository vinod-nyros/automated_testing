from django.core.management.base import NoArgsCommand
import unittest
import random
import string
from django.contrib.auth.models import User, Group
from home.models import *
from django.test import TestCase
from django.test import Client


class Command(NoArgsCommand):
    help = """
    Run the test cases to test the long email  which is more than 35 characters for email field'
    """

    def handle_noargs(self, **options):
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_LongEmail)
        unittest.TextTestRunner().run(suite)

class Test_LongEmail(unittest.TestCase):
    fixtures = ['obdjects.yaml']
    client = Client()
    def setUp(self):
        client = Client()

    def test_contact(self):
        client = Client()
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_contact_long_email(self):
        client = Client()
        unique_string = ''.join(random.choice(string.lowercase) for x in range(10))
        response = client.post(
            "/contact/", {'name': 'test', 'email': 'testemailqwertyuiopasdfghjklzxcvbnm%s@yopmail.com'%unique_string, 'topic': 'Network design services', 'description': 'test', 'body': 'test'})
        self.assertIn("Thank you", response.content)