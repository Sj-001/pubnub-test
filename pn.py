from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from uuid import uuid4

CHANNEL = "MESSAGE"

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-2a31dab6-7c67-4993-a2b7-add1524d3bf8"
pnconfig.subscribe_key = "sub-c-50cce10c-a035-11eb-9adf-f2e9c1644994"
pnconfig.uuid = None

pubnub = PubNub(pnconfig)

class MySubscribeCallback(SubscribeCallback):
  def presence(self, pubnub, event):
    print("[PRESENCE: {}]".format(event.event))
    print("uuid: {}, channel: {}".format(event.uuid, event.channel))

  def status(self, pubnub, event):
    if event.category == PNStatusCategory.PNConnectedCategory:
      print("[STATUS: PNConnectedCategory]")
      print("connected to channels: {}".format(event.affected_channels))

  def message(self, pubnub, event):
    print("[MESSAGE received]")
    print("{}: {}".format(event.message["entry"], event.message["update"]))


pubnub.add_listener(MySubscribeCallback())

pubnub.subscribe().channels(CHANNEL).with_presence().execute()


def publish():
  ENTRY = "Hey"

  message = {"entry": ENTRY, "update": "Hello"}
  envelope = pubnub.publish().channel(CHANNEL).message(message).sync()
  if envelope.status.is_error():
    return "Publish: fail"
  else:
    print("timetoken: %s" % envelope.result.timetoken)

    return "Publish: sent"


