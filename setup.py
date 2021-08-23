# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in xlevel_filling_station/__init__.py
from xlevel_filling_station import __version__ as version

setup(
	name='xlevel_filling_station',
	version=version,
	description='Xlevel Filling Station',
	author='Havenir Solutions',
	author_email='info@havenir.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
