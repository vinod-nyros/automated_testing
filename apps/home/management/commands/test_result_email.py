from django.core.management.base import BaseCommand, CommandError
from subprocess import Popen, PIPE
from django.core.mail import send_mail
from django.conf import settings
from selenium import webdriver
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.template.loader import render_to_string
import os
import socket, urllib2


class Command(BaseCommand):

    help = 'Run the test cases,if tests completed successfully then email a link to the screen shots folder '

    def handle(self, *args, **options):
        process = Popen(['python', 'manage.py', 'test',
                         '--settings=eracks.test_settings'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        hnn = socket.getfqdn()
        my_ip = urllib2.urlopen('http://ip.42.pl/raw').read()
        print hnn
        print my_ip

        if "OK" in stderr:
            print "Test Passed"
            driver = None
            if settings.SELENIUM_DRIVER=='Firefox':
                if settings.FIREFOXPRESENT:
                    driver = True #webdriver.Firefox()
            elif settings.SELENIUM_DRIVER=='Chrome':
                if settings.CHROMEPRESENT:
                    driver = webdriver.Chrome(executable_path=settings.CHROME_DRIVER_PATH)

            if driver:
                #driver.quit()
                subject, from_email = 'Test results for %s, at %s'%(hnn,my_ip), 'support@eracks.com'
                # path=settings.MEDIA_ROOT+"/test_results_screens"
                path_chrome = settings.MEDIA_ROOT+"/test_results_screens/chrome"
                path_firefox = settings.MEDIA_ROOT+"/test_results_screens/firefox"
                # img_list =os.listdir(path)
                img_list_chrome =os.listdir(path_chrome)
                img_list_firefox =os.listdir(path_firefox)
                template_html = 'tested_screens.html'
                text_content = 'Tests completed successfully'
                html_content = render_to_string(template_html, {'chrome_images':img_list_chrome,'firefox_images':img_list_firefox,'hostname':settings.HOST_NAME})
                msg = EmailMultiAlternatives(subject, text_content, from_email, settings.TEST_EMAIL)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
                # send_mail('Tests passed and result screens',
                #       'Tests completed successfully and sending the screens url, url is:%stestresults/' % (settings.HOST_NAME), 'support@eracks.com', settings.TEST_EMAIL, fail_silently=False)
            else:
                print "selenium tests didn't run because browser is not available"
        else:
            print "test failed"
            print stdout
            print stderr
