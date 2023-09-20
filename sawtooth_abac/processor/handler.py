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

import hashlib
import json
import logging

from py_abac import PDP, AccessRequest, Policy
from py_abac.storage.memory import MemoryStorage
from sawtooth_sdk.processor.exceptions import InternalError, InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

from sawtooth_abac.processor.abac_payload import abacPayload
from sawtooth_abac.processor.abac_state import abacState

LOGGER = logging.getLogger(__name__)


class abacTransactionHandler(TransactionHandler):
    # Disable invalid-overridden-method. The sawtooth-sdk expects these to be properties. pylint: disable=invalid-overridden-method
    @property
    def family_name(self):
        return 'abac'

    @property
    def family_versions(self):
        return ['1.0']

    @property
    def namespaces(self):
        return [hashlib.sha512("abac".encode("utf-8")).hexdigest()[0:6]]

    def apply(self, transaction, context):
        header = transaction.header
        signer = header.signer_public_key
        abac_payload = abacPayload.from_bytes(transaction.payload)
        abac_state = abacState(context)

        if abac_payload.action == 'delete':
            if abac_state.get_policy(abac_payload.uid) is None:
                raise InvalidTransaction('Invalid action: policy does not exist')
            abac_state.delete_policy(abac_payload.uid)
        elif abac_payload.action == 'add':
            if abac_state.get_policy(abac_payload.uid) is not None:
                raise InvalidTransaction('Invalid action: Policy already exists: {}'.format(abac_payload.uid))
            abac_state.set_policy(abac_payload.uid, abac_payload.inq)
        elif abac_payload.action == 'check':
            # Setup policy storage
            storage = MemoryStorage()
            # Get all policies of all uids
            policies = abac_state.get_all_policies()
            for uid, policy in policies.items():
                policy["uid"] = uid
                # Parse JSON and create policy objects
                policy = Policy.from_json(policy)
                # Add policy to storage
                storage.add(policy)
            # Create policy decision point
            pdp = PDP(storage)
            # Access request JSON
            request_json = abac_payload.inq
            # Parse JSON and create access request object
            request = AccessRequest.from_json(request_json)
            # Check if access request is allowed
            if pdp.is_allowed(request):
                abac_state.set_check_result(request_json, "1")
                LOGGER.debug("User {} inquiry {} check result: ".format(signer[:6], json.dumps(request_json)) + 'allow\n')
            else:
                abac_state.set_check_result(request_json, "0")
                LOGGER.debug("User {} inquiry {} check result: ".format(signer[:6], json.dumps(request_json)) + 'deny\n')
        else:
            raise InvalidTransaction('Unhandled action: {}'.format(abac_payload.action))
