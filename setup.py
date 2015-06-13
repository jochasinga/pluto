#!/usr/bin/env python

from distutils.core import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='pluto',
    version='0.1.0',
    description="A Python interface for the Firmata protocol",
    long_description=long_description,
    author='Joe Chasinga',
    author_email='jo.chasinga@gmail.com',
    packages=['pluto'],
    include_package_data=True,
    install_requires=['pyserial', 'pyfirmata'],
    zip_safe=False,
    url='https://github.com/jochasinga/pluto',
    download_url = 'https://github.com/jochasinga/pluto/tarball/0.1.0',
    keywords = ['arduino', 'robotics', 'diy', 'iot', 'electronics'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities',
        'Topic :: Home Automation',
    ],
)
    
