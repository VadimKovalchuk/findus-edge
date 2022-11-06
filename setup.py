from setuptools import find_packages, setup

setup(
    name='findus_edge',
    packages=find_packages(include=['findus_edge']),
    install_requires=[
        'finvizfinance==0.14.1',
         'yfinance==0.1.84'
    ],
    version='0.0.1',
    description='Findus edge toolset',
    author='Vadym Kovalchuk',
    license='MIT',
)

