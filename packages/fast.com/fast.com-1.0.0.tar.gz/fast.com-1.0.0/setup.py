from setuptools import setup

setup(
    name='fast.com',
    version='1.0.0',
    description='fast.com speedtest cli',
    long_description=open('readme.md').read(),
    url='https://github.com/banteg/fast',
    author='banteg',
    licence='MIT',
    py_modules=['fast'],
    install_requires=['aiohttp'],
    entry_points={
        'console_scripts': [
            'fast=fast:main',
        ]
    }
)
