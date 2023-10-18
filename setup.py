from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='my_package',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    #test_suite='tests',
)
