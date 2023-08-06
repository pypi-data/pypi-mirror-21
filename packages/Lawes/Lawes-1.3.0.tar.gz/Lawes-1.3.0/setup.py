# -*- coding:utf-8 -*-

from setuptools import setup
from setuptools import find_packages

VERSION = '1.3.0'

setup(
    name='Lawes',
    description='',
    long_description='',
    classifiers=[],
    keywords='',
    author='Lawes',
    author_email='haiou_chen@sina.cn',
    url='https://github.com/MrLawes/Lawes',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'pymongo==2.8',
    ],
    version=VERSION,
)
