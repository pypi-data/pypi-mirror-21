"""
Copyright (c) 2015-2017 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
from setuptools import setup, find_packages

setup(name='python-mystrom',
      version='0.3.7',
      description='Python API for controlling myStrom devices',
      url='https://github.com/fabaff/python-mystrom',
      author='Fabian Affolter',
      author_email='fabian@affolter-engineering.ch',
      license='MIT',
      install_requires=['requests>=2.0'],
      packages=find_packages(),
      zip_safe=True,
      include_package_data=True,
      )
