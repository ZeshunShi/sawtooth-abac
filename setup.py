from __future__ import print_function

import os

from setuptools import setup, find_packages

conf_dir = "/etc/sawtooth"
data_files = [(conf_dir, ['packaging/abac.toml.example'])]

if os.path.exists("/etc/default"):
    data_files.append(('/etc/default', ['packaging/systemd/sawtooth-abac-tp-python']))

if os.path.exists("/lib/systemd/system"):
    data_files.append(('/lib/systemd/system', ['packaging/systemd/sawtooth-abac-tp-python.service']))

setup(
    name='sawtooth-abac',
    version='1.0',
    description='Sawtooth abac Example',
    author='Hyperledger Sawtooth',
    url='https://github.com/hyperledger/sawtooth-sdk-python',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'colorlog',
        'protobuf',
        'sawtooth-sdk',
        'PyYAML',
        'py-abac'
    ],
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'abac = sawtooth_abac.abac_cli:main_wrapper',
            'abac-tp-python = sawtooth_abac.processor.main:main',
            'abac-listener = sawtooth_abac.abac_listener:main'
        ]
    })
