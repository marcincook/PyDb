from importlib.resources import Package

from setuptools import setup, find_packages

# packages=[''],

setup(
    name='PyDb',
    version='1.0.1',
    url='',
    license='',
    author='Marcin D.',
    author_email='marcincook@gmail.com',
    description='',
    packages=find_packages(),
    include_package_data=True,
    cmdclass={
        "package": Package
    }
)
