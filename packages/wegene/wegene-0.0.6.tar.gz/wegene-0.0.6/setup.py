# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


long_description = 'WeGene Python SDK. For details check https://api.wegene.com'

setup(
    name="wegene",
    version="0.0.6",
    url="https://github.com/xraywu/wegene-python-sdk",
    description="WeGene SDK for Python",
    license="MIT",
    author="Eddie Wu",
    author_email="xrayxiaoli@gmail.com",
    package_dir={ 'wegene': 'wegene' },
    packages=find_packages(),
    install_requires=[
        "Unirest==1.1.6",
        "jsonpickle==0.7.1",
        "poster==0.8.1",
    ],
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)
