#!/usr/bin/env python
from setuptools import setup

req = ['nose','numpy','pytz','python-dateutil','xarray','matplotlib']

setup(name='sciencedates',
      packages=['sciencedates'],
      version = '1.2.3',
      description='Date conversions used in the sciences.',
      author = 'Michael Hirsch, Ph.D.',
      url = 'https://github.com/scivision/sciencedates',
      classifiers=[
      'Intended Audience :: Science/Research',
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Topic :: Scientific/Engineering :: GIS',
      'Programming Language :: Python :: 3.5',
      'Programming Language :: Python :: 3.6',
      ],
      install_requires=req
	  )

