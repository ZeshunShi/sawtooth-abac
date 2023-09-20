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

import base64
import json
import random
import time
from base64 import b64encode
from hashlib import sha512
import requests
import yaml

from sawtooth_sdk.protobuf.batch_pb2 import Batch, BatchHeader, BatchList
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction, TransactionHeader
from sawtooth_signing import CryptoFactory, ParseError, create_context
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey

from sawtooth_abac.abac_exceptions import AbacException


def make_address(type, str):
    return sha512("abac".encode()).hexdigest()[:6] + sha512(type.encode()).hexdigest()[:6] + sha512(str.encode()).hexdigest()[:58]


class AbacClient:
    def __init__(self, base_url, keyfile=None):
        self._base_url = base_url
        if keyfile is None:
            self._signer = None
            return
        try:
            with open(keyfile) as fd:
                private_key_str = fd.read().strip()
        except OSError as err:
            raise AbacException('Failed to read private key {}: {}'.format(keyfile, str(err))) from err
        try:
            private_key = Secp256k1PrivateKey.from_hex(private_key_str)
        except ParseError as e:
            raise AbacException('Unable to load private key: {}'.format(str(e))) from e
        self._signer = CryptoFactory(create_context('secp256k1')).new_signer(private_key)

    def add(self, policy, wait=None, auth_user=None, auth_password=None):
        return self._send_abac_txn(action="add", inquiry=policy, wait=wait, auth_user=auth_user, auth_password=auth_password)
    
    def delete(self, policy, wait=None, auth_user=None, auth_password=None):
        return self._send_abac_txn(action="delete", inquiry=policy, wait=wait, auth_user=auth_user, auth_password=auth_password)
    
    def check(self, inquiry, wait=None, auth_user=None, auth_password=None):
        return self._send_abac_txn(action="check", inquiry=inquiry, wait=wait, auth_user=auth_user, auth_password=auth_password)

    def get(self, inquiry, auth_user=None, auth_password=None):
        address = make_address("inquiry", json.dumps(inquiry))
        response = self._send_request("state?address={}".format(address), auth_user=auth_user, auth_password=auth_password)
        encoded_entries = yaml.safe_load(response)["data"]
        try:
            result = encoded_entries[0]["data"]
            if result == "MQ==":
                return "Access"
            elif result == "MA==":
                return "Deny"
            else:
                return "Unknown"
        except:
            return "Unknown"

    def get_all_policies_addresses(self, auth_user=None, auth_password=None):
        address = make_address("policy", "used")
        response = self._send_request("state?address={}".format(address), auth_user=auth_user, auth_password=auth_password)
        result = []
        encoded_entries = yaml.safe_load(response)["data"]
        for entry in encoded_entries:
            result += json.loads(base64.b64decode(entry["data"]).decode())
        return result

    def _create_batch_list(self, transactions):
        transaction_signatures = [t.header_signature for t in transactions]
        header = BatchHeader(signer_public_key=self._signer.get_public_key().as_hex(), transaction_ids=transaction_signatures).SerializeToString()
        signature = self._signer.sign(header)
        batch = Batch(header=header, transactions=transactions, header_signature=signature)
        return BatchList(batches=[batch])

    def _get_status(self, batch_id, wait, auth_user=None, auth_password=None):
        try:
            result = self._send_request('batch_statuses?id={}&wait={}'.format(batch_id, wait), auth_user=auth_user, auth_password=auth_password)
            return yaml.safe_load(result)['data'][0]['status']
        except BaseException as err:
            raise AbacException(err) from err

    def _send_request(self, suffix, data=None, content_type=None, name=None, auth_user=None, auth_password=None):
        if self._base_url.startswith("http://"):
            url = "{}/{}".format(self._base_url, suffix)
        else:
            url = "http://{}/{}".format(self._base_url, suffix)
        headers = {}
        if auth_user is not None:
            headers['Authorization'] = 'Basic {}'.format(b64encode("{}:{}".format(auth_user, auth_password).encode()).decode())
        if content_type is not None:
            headers['Content-Type'] = content_type
        try:
            if data is not None:
                result = requests.post(url, headers=headers, data=data)
            else:
                result = requests.get(url, headers=headers)
            if result.status_code == 404:
                raise AbacException("No such game: {}".format(name))
            if not result.ok:
                raise AbacException("Error {}: {}".format(result.status_code, result.reason))
        except requests.ConnectionError as err:
            raise AbacException('Failed to connect to {}: {}'.format(url, str(err))) from err
        except BaseException as err:
            raise AbacException(err) from err
        return result.text

    def _send_abac_txn(self, action, inquiry, wait=None, auth_user=None, auth_password=None):
        # Construct the address and Serialization is just a delimited utf-8 encoded string
        if action == "check":
            inquiry = json.dumps(inquiry)
            payload = ",".join([action, inquiry]).encode()
            addresses = [make_address("policy", "used"), make_address("inquiry", inquiry)] + self.get_all_policies_addresses()
        else:
            payload = ",".join([action, json.dumps(inquiry)]).encode()
            addresses = [make_address("policy", "used"), make_address("policy", inquiry["uid"])]
        header = TransactionHeader(signer_public_key=self._signer.get_public_key().as_hex(), family_name="abac", family_version="1.0", inputs=addresses, outputs=addresses, dependencies=[], payload_sha512=sha512(payload).hexdigest(), batcher_public_key=self._signer.get_public_key().as_hex(), nonce=hex(random.randint(0, 2**64))).SerializeToString()
        signature = self._signer.sign(header)
        transaction = Transaction(header=header, payload=payload, header_signature=signature)
        batch_list = self._create_batch_list([transaction])
        batch_id = batch_list.batches[0].header_signature
        if wait and wait > 0:
            wait_time = 0
            start_time = time.time()
            response = self._send_request("batches", batch_list.SerializeToString(), 'application/octet-stream', auth_user=auth_user, auth_password=auth_password)
            while wait_time < wait:
                status = self._get_status(batch_id, wait - int(wait_time), auth_user=auth_user, auth_password=auth_password)
                wait_time = time.time() - start_time
                if status != 'PENDING':
                    return response
            return response
        return self._send_request("batches", batch_list.SerializeToString(), 'application/octet-stream', auth_user=auth_user, auth_password=auth_password)
