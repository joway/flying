#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='flying',
    version='0.0.2',
    keywords=('release', 'cli', 'docker', 'git', 'npm'),
    description='Flying : cli tools for manage releases',
    license='MIT License',

    url='https://github.com/joway/flying',
    author='joway',
    author_email='joway.w@gmail.com',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    platforms='any',
    install_requires=[
        'fire==0.1.3',
        'twine==1.11.0',
    ],
    entry_points={
        'console_scripts': [
            'flying=flying.main:main'
        ]
    },
)
