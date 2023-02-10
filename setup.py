# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name='ontoply',
    version='0.0.1',
    description='Methods to manipulate ontologies',
    url='https://github.com/aiaragomes/ontologies',
    license='MIT License',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'Owlready2>=0.40'
    ]
)
