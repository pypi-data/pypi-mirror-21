# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup, find_packages
import codecs


def _read_file(name, encoding='utf-8'):
    """
    Read the contents of a file.

    :param name: The name of the file in the current directory.
    :param encoding: The encoding of the file; defaults to utf-8.
    :return: The contents of the file.
    """
    with codecs.open(name, encoding=encoding) as f:
        return f.read()


setup(
    name='stitcher',
    version='0.0.1',
    description='Join Messenger conversation screenshots.',
    long_description=_read_file('README.rst'),
    license='MIT',
    url='https://github.com/gebn/stitcher',
    author='George Brighton',
    author_email='oss@gebn.co.uk',
    packages=find_packages(),
    zip_safe=True,
    install_requires=[
        'six>=1.9.0',
        'Pillow'
    ],
    test_suite='nose.collector',
    tests_require=[
        'nose'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': [
            'stitch = stitcher.__main__:main_cli',
        ]
    }
)
