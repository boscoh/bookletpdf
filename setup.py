#!/usr/bin/env python
from setuptools import setup

description = "Docs at http://github.com/boscoh/booklet"

setup(
    name='booklet',
    version='0.5',
    author='Bosco Ho',
    author_email='boscoh@gmail.com',
    url='http://github.com/boscoh/booklet',
    description='simple object to make reportlab pdf',
    long_description=description,
    license='BSD',
    install_requires=['reportlab', 'pillow'],
    py_modules=['booklet'],
    scripts=[]
)
