#!/usr/bin/env python
import sys
from setuptools import setup, find_packages

long_description = open('README.rst').read()

setup(name="scrapelib",
      version='1.0.1',
      py_modules=['scrapelib'],
      author="James Turk",
      author_email='james.p.turk@gmail.com',
      license="BSD",
      url="http://github.com/jamesturk/scrapelib",
      long_description=long_description,
      packages=find_packages(),
      description="a library for scraping things",
      platforms=["any"],
      classifiers=["Development Status :: 6 - Mature",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
      install_requires=['requests[security]>=2'],
      entry_points="""
[console_scripts]
scrapeshell = scrapelib.__main__:scrapeshell
"""
      )
