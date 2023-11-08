from setuptools import find_packages, setup

setup(
    name='findus_edge',
    packages=find_packages(),
    install_requires=[
        'finvizfinance==0.14.7',
         'yfinance==0.2.28'
    ],
    version='0.0.1',
    description='Findus edge toolset',
    author='Vadym Kovalchuk',
    license='MIT',
)

