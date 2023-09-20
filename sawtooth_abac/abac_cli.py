# Copyright 2018 Intel Corporation
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
# -----------------------------------------------------------------------------

from __future__ import print_function

import argparse
import getpass
import json
import logging
import os
import sys
import traceback

import pkg_resources
from colorlog import ColoredFormatter

from sawtooth_abac.abac_client import AbacClient
from sawtooth_abac.abac_exceptions import AbacException

DISTRIBUTION_NAME = 'sawtooth-abac'
DEFAULT_URL = 'http://127.0.0.1:8008'


def create_console_handler(verbose_level):
    clog = logging.StreamHandler()
    formatter = ColoredFormatter("%(log_color)s[%(asctime)s %(levelname)-8s%(module)s]%(reset)s %(white)s%(message)s", datefmt="%H:%M:%S", reset=True, log_colors={'DEBUG':'cyan','INFO':'green','WARNING':'yellow','ERROR':'red','CRITICAL':'red'})
    clog.setFormatter(formatter)
    if verbose_level == 0:
        clog.setLevel(logging.WARN)
    elif verbose_level == 1:
        clog.setLevel(logging.INFO)
    else:
        clog.setLevel(logging.DEBUG)
    return clog


def setup_loggers(verbose_level):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(create_console_handler(verbose_level))


def add_add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('add', help='Add a new abac policy', description='Sends a transaction to add an abac policy.', parents=[parent_parser])
    parser.add_argument('filename', type=str, help='filename for the new policy')
    parser.add_argument('--url', type=str, help='specify URL of REST API')
    parser.add_argument('--user', type=str, help="identify name of user's private key file")
    parser.add_argument('--key-dir', type=str, help="identify directory of user's private key file")
    parser.add_argument('--auth-user', type=str, help='specify username for authentication if REST API is using Basic Auth')
    parser.add_argument('--auth-password', type=str, help='specify password for authentication if REST API is using Basic Auth')
    parser.add_argument('--disable-client-validation', action='store_true', default=False, help='disable client validation')
    parser.add_argument('--wait', nargs='?', const=sys.maxsize, type=int, help='set time, in seconds, to wait for game to commit')


def add_delete_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('delete', help='Delete a used abac policy', description='Sends a transaction to delete an abac policy.', parents=[parent_parser])
    parser.add_argument('filename', type=str, help='filename for the used policy')
    parser.add_argument('--url', type=str, help='specify URL of REST API')
    parser.add_argument('--user', type=str, help="identify name of user's private key file")
    parser.add_argument('--key-dir', type=str, help="identify directory of user's private key file")
    parser.add_argument('--auth-user', type=str, help='specify username for authentication if REST API is using Basic Auth')
    parser.add_argument('--auth-password', type=str, help='specify password for authentication if REST API is using Basic Auth')
    parser.add_argument('--disable-client-validation', action='store_true', default=False, help='disable client validation')
    parser.add_argument('--wait', nargs='?', const=sys.maxsize, type=int, help='set time, in seconds, to wait for game to commit')


def add_check_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('check', help='check a inquiry', description='Sends a transaction to check an abac inquiry.', parents=[parent_parser])
    parser.add_argument('filename', type=str, help='filename for the inquiry')
    parser.add_argument('--url', type=str, help='specify URL of REST API')
    parser.add_argument('--user', type=str, help="identify name of user's private key file")
    parser.add_argument('--key-dir', type=str, help="identify directory of user's private key file")
    parser.add_argument('--auth-user', type=str, help='specify username for authentication if REST API is using Basic Auth')
    parser.add_argument('--auth-password', type=str, help='specify password for authentication if REST API is using Basic Auth')
    parser.add_argument('--disable-client-validation', action='store_true', default=False, help='disable client validation')
    parser.add_argument('--wait', nargs='?', const=sys.maxsize, type=int, help='set time, in seconds, to wait for game to commit')


def add_get_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('get', help='get a inquiry check result', description='Sends a request to get an abac inquiry check result.', parents=[parent_parser])
    parser.add_argument('filename', type=str, help='filename for the inquiry')
    parser.add_argument('--url', type=str, help='specify URL of REST API')
    parser.add_argument('--auth-user', type=str, help='specify username for authentication if REST API is using Basic Auth')
    parser.add_argument('--auth-password', type=str, help='specify password for authentication if REST API is using Basic Auth')
    parser.add_argument('--disable-client-validation', action='store_true', default=False, help='disable client validation')


def create_parent_parser(prog_name):
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
    parent_parser.add_argument('-v', '--verbose', action='count', help='enable more verbose output')
    try:
        version = pkg_resources.get_distribution(DISTRIBUTION_NAME).version
    except pkg_resources.DistributionNotFound:
        version = 'UNKNOWN'
    parent_parser.add_argument('-V', '--version', action='version', version=(DISTRIBUTION_NAME+' (Hyperledger Sawtooth) version {}').format(version), help='display version information')
    return parent_parser


def create_parser(prog_name):
    parent_parser = create_parent_parser(prog_name)
    parser = argparse.ArgumentParser(description='Provides subcommands to play abac by sending ABAC transactions.', parents=[parent_parser])
    subparsers = parser.add_subparsers(title='subcommands', dest='command')
    subparsers.required = True
    add_add_parser(subparsers, parent_parser)
    add_delete_parser(subparsers, parent_parser)
    add_check_parser(subparsers, parent_parser)
    add_get_parser(subparsers, parent_parser)
    return parser


def do_add(args):
    policy = open(args.filename, 'r')
    policy = policy.read()
    policy = json.loads(policy)
    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user, auth_password = _get_auth_info(args)
    client = AbacClient(base_url=url, keyfile=keyfile)
    if args.wait and args.wait > 0:
        response = client.add(policy, wait=args.wait, auth_user=auth_user, auth_password=auth_password)
    else:
        response = client.add(policy, auth_user=auth_user, auth_password=auth_password)
    print("Response: {}".format(response))


def do_delete(args):
    policy = open(args.filename, 'r')
    policy = policy.read()
    policy = json.loads(policy)
    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user, auth_password = _get_auth_info(args)
    client = AbacClient(base_url=url, keyfile=keyfile)
    if args.wait and args.wait > 0:
        response = client.delete(policy, wait=args.wait, auth_user=auth_user, auth_password=auth_password)
    else:
        response = client.delete(policy, auth_user=auth_user, auth_password=auth_password)
    print("Response: {}".format(response))


def do_check(args):
    inquiry = open(args.filename, 'r')
    inquiry = inquiry.read()
    inquiry = json.loads(inquiry)
    url = _get_url(args)
    keyfile = _get_keyfile(args)
    auth_user, auth_password = _get_auth_info(args)
    client = AbacClient(base_url=url, keyfile=keyfile)
    if args.wait and args.wait > 0:
        response = client.check(inquiry, wait=args.wait, auth_user=auth_user, auth_password=auth_password)
    else:
        response = client.check(inquiry, auth_user=auth_user, auth_password=auth_password)
    print("Response: {}".format(response))


def do_get(args):
    inquiry = open(args.filename, 'r')
    inquiry = inquiry.read()
    inquiry = json.loads(inquiry)
    url = _get_url(args)
    auth_user, auth_password = _get_auth_info(args)
    client = AbacClient(base_url=url, keyfile=None)
    response = client.get(inquiry, auth_user=auth_user, auth_password=auth_password)
    print("Result: {}".format(response))


def _get_url(args):
    return DEFAULT_URL if args.url is None else args.url


def _get_keyfile(args):
    user = getpass.getuser() if args.user is None else args.user
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")
    return '{}/{}.priv'.format(key_dir, user)


def _get_auth_info(args):
    auth_user = args.auth_user
    auth_password = args.auth_password
    if auth_user is not None and auth_password is None:
        auth_password = getpass.getpass(prompt="Auth Password: ")
    return auth_user, auth_password


def main(prog_name=os.path.basename(sys.argv[0]), args=None):
    if args is None:
        args = sys.argv[1:]
    parser = create_parser(prog_name)
    args = parser.parse_args(args)
    if args.verbose is None:
        verbose_level = 0
    else:
        verbose_level = args.verbose
    setup_loggers(verbose_level=verbose_level)
    if args.command == 'add':
        do_add(args)
    elif args.command == 'delete':
        do_delete(args)
    elif args.command == 'check':
        do_check(args)
    elif args.command == 'get':
        do_get(args)
    else:
        raise AbacException("invalid command: {}".format(args.command))


def main_wrapper():
    try:
        main()
    except AbacException as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
