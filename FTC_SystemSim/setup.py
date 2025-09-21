
from setuptools import setup, find_packages

setup(
  name = 'FTC_SystemSim',
  version='0.1',
  description="FTC_SystemSim is a system level tradeoff analysis tool for FTC",
  author="Soumitra Borthakur",
  packages=find_packages(),
  install_requires=[
          'numpy',
          'time',
          'matplotlib'
      ],
)


