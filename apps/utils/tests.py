from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Group

class ViewsTests(TestCase):
    def setUp(self):
            user1 = User.objects.create_superuser(
                username="admin_eracks", email="admin_eracks@yopmail.com", password="admin_eracks")
    def test_urls(self):
        client = Client()
        response1 = client.post(
            "/accounts/login/", {'identification': 'admin_eracks', 'password': 'admin_eracks'})
        response = client.get("/utils/urls/")
        self.assertEqual(response.status_code, 200)

    def test_clearcache(self):
        client = Client()
        response = client.get("/utils/clearcache")
        self.assertEqual(response.status_code, 200)

def find_first(selenium, *selector_list):
    for sel in selector_list:
        try:
            elm = selenium.find_element_by_css_selector (sel)
            return elm
        except Exception,e:
            if e: print e
    raise Exception ("No selector matches")
