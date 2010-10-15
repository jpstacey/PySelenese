# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

setup(name='selenese',
      version='0.0.1',
      description="Python Selenese translator",
      long_description=open('README').read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Intended Audience :: Developers',
        ],
      keywords='',
      author='J-P Stacey',
      author_email='',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        # -*- Extra requirements: -*-
                        ],
      entry_points="""
      # -*- entry_points -*- 
      """,
      )
