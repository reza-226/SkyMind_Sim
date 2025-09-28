# setup.py
from setuptools import setup, find_packages

setup(
    name='skymind_sim',
    version='0.1.0',
    packages=find_packages(),
    author='Reza', # Or your name
    author_email='your_email@example.com', # Optional
    description='A simple drone flight simulator.',
    long_description=open('README.md').read(),
)
