#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import absolute_import,division,print_function,unicode_literals

from setuptools import setup, find_packages

setup(name = 'Kubos',
      version = '0.2b',
      description = 'Simple CAD Modelling Application',
      author = 'Marko Knöbl',
      author_email = 'marko.kn@gmail.com',
      url = 'http://sourceforge.net/p/kubos',
      packages = find_packages(),
      include_package_data = True,
      )
