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
import sys

import zmq
from google.protobuf import json_format
from sawtooth_sdk.protobuf.client_event_pb2 import ClientEventsSubscribeRequest, ClientEventsSubscribeResponse, ClientEventsUnsubscribeRequest, ClientEventsUnsubscribeResponse
from sawtooth_sdk.protobuf.events_pb2 import EventList, EventSubscription
from sawtooth_sdk.protobuf.validator_pb2 import Message


def main():
    # Setup a connection to the validator
    ctx = zmq.Context()
    socket = ctx.socket(zmq.DEALER)
    socket.connect(sys.argv[1])
    # Construct the request
    request = ClientEventsSubscribeRequest(subscriptions=[EventSubscription(event_type="abac/result")]).SerializeToString()
    # Construct the message wrapper. The correlation_id must be unique for all in-process requests
    msg = Message(correlation_id="subscribe", message_type=Message.CLIENT_EVENTS_SUBSCRIBE_REQUEST, content=request)
    # Send the serialized message to the validator
    socket.send_multipart([msg.SerializeToString()])
    # Receive the response
    resp = socket.recv_multipart()[-1]
    # Parse the message wrapper
    msg = Message()
    msg.ParseFromString(resp)
    # Validate the response type
    if msg.message_type != Message.CLIENT_EVENTS_SUBSCRIBE_RESPONSE:
        print("NOT CLIENT EVENTS SUBSCRIBE RESPONSE")
    # Parse the response
    response = ClientEventsSubscribeResponse()
    response.ParseFromString(msg.content)
    # Validate the response status
    if response.status != ClientEventsSubscribeResponse.OK:
        print("Subscription failed: {}".format(response.response_message))
    # Listening messages from the validator
    try:
        while True:
            # Receive the response
            resp = socket.recv_multipart()[-1]
            # Parse the message wrapper
            msg = Message()
            msg.ParseFromString(resp)
            # Validate the response type
            if msg.message_type == Message.CLIENT_EVENTS:
                # Parse the response
                events = EventList()
                events.ParseFromString(msg.content)
                for event in events.events:
                    event = json_format.MessageToJson(event)
                    event = json.loads(event)
                    event = event["attributes"]
                    inquiry, result = event[0], event[1]
                    inquiry = inquiry["value"]
                    result = result["value"]
                    decision = {"inquiry": inquiry, "result": result}
                    print("decision =", decision)
    except:
        # Construct the request
        request = ClientEventsUnsubscribeRequest().SerializeToString()
        # Construct the message wrapper
        msg = Message(correlation_id="unsubscribe", message_type=Message.CLIENT_EVENTS_UNSUBSCRIBE_REQUEST, content=request)
        # Send the request
        socket.send_multipart([msg.SerializeToString()])
        # Receive the response
        resp = socket.recv_multipart()[-1]
        # Parse the message wrapper
        msg = Message()
        msg.ParseFromString(resp)
        # Validate the response type
        if msg.message_type != Message.CLIENT_EVENTS_UNSUBSCRIBE_RESPONSE:
            print("Unexpected message type")
        # Parse the response
        response = ClientEventsUnsubscribeResponse()
        response.ParseFromString(msg.content)
        # Validate the response status
        if response.status != ClientEventsUnsubscribeResponse.OK:
            print("Unsubscription failed: {}".format(response.response_message))
        # Close the connection to the validator
        socket.close()