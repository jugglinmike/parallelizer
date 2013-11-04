#!/usr/bin/env python

from setuptools import setup

setup(name = 'parallelizer',
      version = '0.0.1',
      description = 'A tool for efficiently scheduling test execution',
      author = 'Mike Pennisi',
      author_email = 'mike@mikepennisi.com',
      url = 'https://github.com/jugglinmike/parallelizer',
      packages = ['parallelizer'],
      install_requires = ['mozprocess>=0.13'],
      entry_points = {
        'console_scripts': [
            'parallelizer = parallelizer.parallelizer:cli'
        ]
      }
      )
