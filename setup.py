import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-wedsite',
    version='0.0.10',
    packages=find_packages(),
    include_package_data=True,
    license="GPLv3",
    description='A simple open-source django wedding website',
    long_description=README,
    url='https://www.wedsite.io/',
    author='Dan Pipe-Mazo',
    author_email='dpipemazo@gmail.com',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',  # replace "X.Y" as appropriate
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only ',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],


    # Installation Requirements
    install_requires = [
        "dj-database-url==0.4.1",
        "Django==1.11",
        "gunicorn==19.6.0",
        "psycopg2==2.7.3",
        "whitenoise==3.3.0",
        "requests==2.9.1",
        "django-easy-maps==0.9.3",
        "raven>=3",
        "django-tz-detect==0.2.8",
        "django-inlinecss==0.1.2",
        "lorem",
        "django-appconf",
    ],
)
