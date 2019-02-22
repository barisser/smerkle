from setuptools import find_packages, setup

setup(name='smerkle',
      version='0.0.1',
      description='',
      url='http://github.com/barisser/smerkle',
      author='Andrew Barisser',
      author_email='barisser@protonmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            'ecdsa>=0.13',
            'pybitcoin',
            'pycrypto'
      ]
      )
