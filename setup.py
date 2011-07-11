#!/usr/bin/env python

from distutils.core import setup

from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None
setup(name = 'django-stripe',
        version = '0.1',
        description = 'A user subscription Django app that integrates with Stripe (http://stripe.com/)',
        author = 'Andrew McCloud',
        author_email = 'andrew@amccloud.com',
        url = 'https://github.com/amccloud/django-stripe/',
        classifiers = [
              'Programming Language :: Python :: 2',
           ],
        packages = ['./django_stripe'],
        package_dir = {'./django_stripe': 'django_stripe'},
        )
