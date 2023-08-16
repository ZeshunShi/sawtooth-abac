from google.protobuf import json_format
import json
import zmq
import sys
from sawtooth_sdk.protobuf.client_event_pb2 import ClientEventsSubscribeRequest, ClientEventsSubscribeResponse
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
    msg = Message(correlation_id="abac/result", message_type=Message.CLIENT_EVENTS_SUBSCRIBE_REQUEST, content=request)
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