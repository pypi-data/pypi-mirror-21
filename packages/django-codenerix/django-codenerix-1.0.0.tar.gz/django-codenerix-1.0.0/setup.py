import os
from setuptools import setup

#from setuptools.command.install import install
#class CustomInstallCommand(install):
#    """Customized setuptools install command - prints a friendly greeting."""
#    def run(self):
#        print "Hello, developer, how are you? :)"
#        install.run(self)
#        #post-processing code

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-codenerix',
    version="1.0.0",
    packages=['codenerix'],
    include_package_data=True,
    zip_safe=False,
    license='Apache License Version 2.0',
    description='Codenerix it is a framework that goes on top of Django so it makes easier development and building of ERPs.',
    long_description=README,
    url='https://github.com/centrologic/django-codenerix',
    author='Juan Miguel Taboada Godoy',
    author_email='juanmi@centrologic.com',
    keywords=['django', 'codenerix', 'management','erp','crm'],
    platforms=['OS Independent'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    # cmdclass={ 'install': CustomInstallCommand, },
    install_requires = [
        "pymongo==3.4.0",
        "django-angular==0.8.4",
        "python-dateutil==2.6.0",
        "django-recaptcha==1.2.1",
        "django-rosetta==0.7.6",
        "jsonfield==1.0.3",
        "openpyxl==2.2.5",
        "Pillow==2.6.1",
        "Unidecode==0.4.20",
        "xhtml2pdf==0.0.6",
        "Django==1.10.6",
        "django-multi-email-field",
        "ldap3",
        ],
)

