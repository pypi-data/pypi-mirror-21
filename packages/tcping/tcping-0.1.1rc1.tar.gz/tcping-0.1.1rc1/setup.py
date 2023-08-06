#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


with open("tcping.py") as fp:
    for line in fp:
        if line.startswith("__version__"):
            __version__ = line.split("=")[1].strip(" \"'\r\n")
            break
    else:
        from tcping import __version__


def read_long_description():
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError, RuntimeError):
        return ""


setup(
    name='tcping',
    version=__version__,
    author='zhengxiaowai',
    author_email='h1x2y3awalm@gmail.com',
    long_description=read_long_description(),
    url='https://github.com/kontspace/tcping',
    description='command line for tcp ping',
    license='MIT',
    keywords='python tcp ping',
    py_modules=['tcping'],
    scripts=['tcping.py'],
    install_requires=['six', 'click', 'prettytable'],
    entry_points={
        'console_scripts': ['tcping = tcping:cli']
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
        "Topic :: System"
    ]
) 
