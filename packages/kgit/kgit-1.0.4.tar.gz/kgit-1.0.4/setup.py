from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kgit',
    version='1.0.4',
    description='Commonly used git convenience functionality for todays modern developer.',
    long_description=long_description,
    url='https://github.com/kris-nova/kgit',
    author='Kris Nova',
    author_email='kris@nivenly.com',
    license='MIT',
    packages=['kgit', ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Environment :: MacOS X',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='git, config, wrapper, manager',
    entry_points={
        'console_scripts': ['kgit=kgit.kgit:main', ],
    },
)
