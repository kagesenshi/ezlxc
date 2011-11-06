from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='ezlxc',
      version=version,
      description="Easy Linux Container",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Izhar Firdaus',
      author_email='kagesenshi.87@gmail.com',
      url='http://blog.kagesenshi.org',
      license='GPLv2+',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
         'argh'
          # -*- Extra requirements: -*-
      ],
      entry_points={
        'console_scripts': [
            'ezlxc-admin = ezlxc.scripts:main',
        ]
      }
)
