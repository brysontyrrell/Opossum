import re
from setuptools import find_packages, setup

regex = re.compile(r'^__\w+__\s*=.*$')

about = dict()
with open('possum', 'r') as f:
    dunders = list()
    for l in f.readlines():
        if regex.match(l):
            dunders.append(l)
    exec('\n'.join(dunders), about)

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    version=about['__version__'],
    description='A module of decorators and utilities for Python AWS serverless applications.',
    long_description=readme,
    author=about['__author__'],
    author_email=about['__author_email__'],
    url='https://github.com/brysontyrrell/Opossum',
    license=about['__license__'],
    python_requires='>=3.6',
    packages=find_packages(),
    install_requires=[
        'jsonschema>=2.6.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6'
    ]
)
