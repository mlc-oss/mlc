import os

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r') as f:
      requirements = f.readlines()

setup(name='mlc',
      version='0.1.0',
      install_requires=requirements)
