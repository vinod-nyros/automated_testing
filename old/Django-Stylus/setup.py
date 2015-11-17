from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


README = read('README.rst')
CHANGES = read('CHANGES.rst')


setup(
    name = "Django-Stylus",
    packages = find_packages(),
    version = "0.1",
    author = "Joseph Wolff",
    author_email = "joe@osdf.com",
    url = "https://github.com/jowolf/Django-Stylus",
    description = "Django template tags to compile Stylus",
    long_description = "\n\n".join([README, CHANGES]),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = ["stylus","less","css","sass","compass","django","python",],
)
