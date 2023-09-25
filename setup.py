# Copyright 2017 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

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
    description='Sawtooth ABAC Example',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.0.1',
        'colorlog==3.1.2',
        'protobuf==3.6.1',
        'sawtooth-sdk==1.2.5',
        'PyYAML==3.12',
        'requests==2.18.4',
        'py-abac==0.4.1',
        'pyzmq==16.0.2'
    ],
    data_files=data_files,
    entry_points={
        'console_scripts': [
            'abac = sawtooth_abac.abac_cli:main_wrapper',
            'abac-tp-python = sawtooth_abac.processor.main:main',
            'abac-listener = sawtooth_abac.abac_listener:main'
        ]
    })
