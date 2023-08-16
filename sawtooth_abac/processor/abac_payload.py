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
