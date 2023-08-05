#! /usr/bin/env python

from setuptools import setup

CLASSIFIERS = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Developers',
	'License :: OSI Approved :: MIT License',
	'Operating System :: OS Independent',
	'Programming Language :: Python',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
	'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
	name='pokinator',
	author='punkyoon',
	author_email='punkkid001@gmail.com',
	keywords='random pokemon name generator',
	description='Heroku-like random pokemon name generator for python',
	license='MIT',
	version='1.1.2',
	url='https://github.com/punkyoon/pokinator',
	packages=['pokinator', 'pokinator/pokemons'],
	test_suite='pokinator.tests',
	include_package_data=True,
	classifiers=CLASSIFIERS,
	platforms=['any']
)

