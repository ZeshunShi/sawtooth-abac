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

from sawtooth_sdk.processor.exceptions import InvalidTransaction


class abacPayload:
    def __init__(self, payload):
        try:
            # The payload is csv utf-8 encoded string
            action, inq = payload.decode().split(",", 1)
            inq = json.loads(inq)
        except ValueError as e:
            raise InvalidTransaction("Invalid payload serialization") from e

        if not action:
            raise InvalidTransaction('Action is required')
        if action not in ('add', 'delete', 'check'):
            raise InvalidTransaction('Invalid action: {}'.format(action))
        if action == 'check':
            for e in inq:
                if e not in ('subject', 'resource', 'action', 'context'):
                    raise InvalidTransaction('Invalid inquiry: {}'.format(inq))
        else:
            for e in inq:
                if e not in ("uid", "description", "effect", "rules", "targets", "priority"):
                    raise InvalidTransaction('Invalid policy: {}'.format(inq))

        self._action = action
        if "uid" in inq:
            self._uid = inq["uid"]
            del inq["uid"]
            self._inq = inq
        else:
            self._uid = None
            self._inq = inq

    @staticmethod
    def from_bytes(payload):
        return abacPayload(payload=payload)

    @property
    def action(self):
        return self._action
    
    @property
    def uid(self):
        return self._uid

    @property
    def inq(self):
        return self._inq
