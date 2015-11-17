from django.core.management.base import NoArgsCommand
import unittest
from django.contrib.auth.models import User, Group
from home.models import *
from django.test import TestCase
from django.test import Client


class Command(NoArgsCommand):
    help = """
    If you need Arguments, please check other modules in 
    django/core/management/commands.
    """

    def handle_noargs(self, **options):
        suite = unittest.TestLoader().loadTestsFromTestCase(LongEmail)
        unittest.TextTestRunner().run(suite)

class LongEmail(unittest.TestCase):
    fixtures = ['obdjects.yaml']
    client = Client()
    def setUp(self):
        client = Client()

    def test_user_signup_post(self):
        client = Client()
        response = client.post(
            "/accounts/signup/", {'username': 'test1235', 'email': 'test1235@yopmail.com'})
        self.assertIn("Thank you", response.content)


    def test_user_login(self):
        client = Client()
        response = client.post(
            "/accounts/login/", {'identification': 'testmailname1', 'password': 'testuser1'}, follow=True)
        self.assertIn("You have been signed in", response.content)


    def test_contact(self):
        client = Client()
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_contact_post(self):
        client = Client()
        response = client.post(
            "/contact/", {'name': 'test', 'email': 'test@yopmail.com', 'topic': 'NETWORK-DESIGN', 'description': 'test', 'body': 'test'})
        self.assertIn("Thank you", response.content)


    def test_contact_long_email(self):
        client = Client()
        response = client.post(
            "/contact/", {'name': 'test', 'email': 'lengthentestindevwithverylargeemailid@yopmail.com', 'topic': 'NETWORK-DESIGN', 'description': 'test', 'body': 'test'})
        self.assertIn("Thank you", response.content)


