#!/usr/bin/env python3
import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='flying',
    version='0.0.6',
    keywords=('release', 'cli', 'docker', 'git', 'npm', 'pypi'),
    description='Cli tools for manage releases',
    license='MIT License',

    url='https://github.com/joway/flying',
    author='joway',
    author_email='joway.w@gmail.com',

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    platforms='any',
    long_description=read('README.md'),
    install_requires=[
        'fire==0.1.3',
        'twine==3.0.0',
    ],
    entry_points={
        'console_scripts': [
            'flying=flying.main:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Version Control',
    ],
)
