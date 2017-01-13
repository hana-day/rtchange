import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(here, 'README.md')) as f:
        README = f.read()
except IOError:
    README = ''

install_requires = [
    'numpy',
]

tests_require = [
    'pytest',
    'flake8',
]

setup(
    name='rtchange',
    version='0.0.1',
    description='Real-time change point detection',
    long_description=README,
    classifiers=[
    ],
    author="Yusuke Hanada",
    author_email="hyusuk9872@gmail.com",
    license="The MIT License (https://opensource.org/licenses/MIT)",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        "testing": tests_require,
    },
    test_suite="rtchange.tests",
)
