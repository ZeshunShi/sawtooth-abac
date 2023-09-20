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

import json
from hashlib import sha512

from sawtooth_sdk.processor.exceptions import InternalError


def make_address(type, str):
    return sha512("abac".encode()).hexdigest()[:6] + sha512(type.encode()).hexdigest()[:6] + sha512(str.encode()).hexdigest()[:58]


class abacState:

    TIMEOUT = 3
    POLICIES_USED = make_address("policy", "used")

    def __init__(self, context):
        """Constructor.
        Args:
            context (sawtooth_sdk.processor.context.Context): Access to validator state from within the transaction processor.
        """
        self._context = context
        self._address_cache = {}

    def delete_policy(self, policy_uid):
        """Delete the Policy named policy_uid from state.
        Args:
            policy_uid (str): The uid.
        Raises:
            KeyError: The Policy with policy_uid does not exist.
        """
        policies = self._load_policies(policy_uid=policy_uid)
        del policies[policy_uid]
        if policies:
            self._store_policy(policy_uid, policies=policies)
        else:
            self._delete_policy(policy_uid)

    def set_policy(self, policy_uid, policy):
        """Store the policy in the validator state.
        Args:
            policy_uid (str): The uid.
            policy (Policy): The information specifying the current policy.
        """
        policies = self._load_policies(policy_uid=policy_uid)
        policies[policy_uid] = policy
        self._store_policy(policy_uid, policies=policies)

    def get_policy(self, policy_uid):
        """Get the policy associated with policy_uid.
        Args:
            policy_uid (str): The uid.
        Returns:
            (Policy): All the information specifying a policy.
        """
        return self._load_policies(policy_uid=policy_uid).get(policy_uid)

    def get_all_policies(self):
        """Get all policies.
        Returns:
            (dict): policy uid (str) keys, Policy details.
        """
        used_addresses = self._get_used_addresses()
        policies = {}
        entries = self._context.get_state(used_addresses, timeout=self.TIMEOUT)
        for entry in entries:
            policies.update(self._deserialize(entry.data))
        return policies

    def _get_used_addresses(self):
        used_addresses = self._context.get_state([self.POLICIES_USED], timeout=self.TIMEOUT)
        if len(used_addresses):
            return json.loads(used_addresses[0].data.decode())
        else:
            return []
    
    def _set_used_addresses(self, used_addresses):
        self._context.set_state({self.POLICIES_USED: json.dumps(used_addresses).encode()}, timeout=self.TIMEOUT)

    def _store_policy(self, policy_uid, policies):
        address = make_address("policy", policy_uid)
        state_data = self._serialize(policies)
        self._address_cache[address] = state_data
        self._context.set_state({address: state_data}, timeout=self.TIMEOUT)
        used_addresses = self._get_used_addresses()
        used_addresses.append(address)
        self._set_used_addresses(used_addresses=used_addresses)


    def _delete_policy(self, policy_uid):
        address = make_address("policy", policy_uid)
        self._context.delete_state([address], timeout=self.TIMEOUT)
        self._address_cache[address] = None
        used_addresses = self._get_used_addresses()
        used_addresses.remove(address)
        self._set_used_addresses(used_addresses=used_addresses)

    def _load_policies(self, policy_uid):
        address = make_address("policy", policy_uid)
        if address in self._address_cache:
            if self._address_cache[address]:
                serialized_policies = self._address_cache[address]
                policies = self._deserialize(serialized_policies)
            else:
                policies = {}
        else:
            entries = self._context.get_state([address], timeout=self.TIMEOUT)
            if entries:
                self._address_cache[address] = entries[0].data
                policies = self._deserialize(data=entries[0].data)
            else:
                self._address_cache[address] = None
                policies = {}
        return policies

    def _deserialize(self, data):
        """Take bytes stored in state and deserialize them into Python Policy objects.
        Args:
            data (bytes): The UTF-8 encoded string stored in state.
        Returns:
            (dict): policy uid (str) keys, Policy details.
        """
        policies = {}
        try:
            for policy in data.decode().split("|"):
                uid, p = policy.split(",", 1)
                policies[uid] = json.loads(p)
        except ValueError as e:
            raise InternalError("Failed to deserialize policy data") from e
        return policies

    def _serialize(self, policies):
        """Takes a dict of policy objects and serializes them into bytes.
        Args:
            policies (dict): policy uid (str) keys, Policy details.
        Returns:
            (bytes): The UTF-8 encoded string stored in state.
        """
        policy_strs = []
        for uid, p in policies.items():
            policy_str = ",".join([uid, json.dumps(p)])
            policy_strs.append(policy_str)
        return "|".join(sorted(policy_strs)).encode()

    def set_check_result(self, inquiry, result):
        """Store the inquiry check result in the validator state.
        Args:
            inquiry (dict): inquiry details.
        """
        address = make_address("inquiry", json.dumps(inquiry))
        self._context.set_state({address: result.encode()}, timeout=self.TIMEOUT)
        self._context.add_event("abac/result", [("inquiry",json.dumps(inquiry)),("result",result)])

    def get_check_result(self, inquiry):
        """Get the inquiry check result in the validator state.
        Args:
            inquiry (dict): inquiry details.
        Returns:
            (str): The result string stored in state.
        """
        address = make_address("inquiry", json.dumps(inquiry))
        entries = self._context.get_state([address], timeout=self.TIMEOUT)
        if entries:
            return entries[0].data.decode()
        return ""
