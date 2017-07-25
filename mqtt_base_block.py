from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty, IntProperty
from nio.util.discovery import not_discoverable

import paho.mqtt.client as mqtt


@not_discoverable
class MqttBase(Block):

    version = VersionProperty('0.1.0')
    client_id = StringProperty(title="Client ID", default="", allow_none=False)
    port = IntProperty(title="Port", default=1883, allow_none=False)
    host = StringProperty(title="Host", default="localhost", allow_none=False)
    topic = StringProperty(title="Topic", default="", allow_none=False)

    def __init__(self):
        super().__init__()
        self.client = None

    def configure(self, context):
        super().configure(context)
        self.client = mqtt.Client(self.client_id())
        self.connect()
        self.client.loop_start()

    def stop(self):
        self.disconnect()
        super().stop()

    def connect(self):
        self.logger.debug("Connecting...")
        self.client.on_connect = self.on_connect
        self.client.connect(self.host(), self.port())

    def on_connect(self, client, userdata, rc):
        self.logger.debug("Connected with result code {}".format(self.client.connack_string(rc)))

    def disconnect(self):
        self.logger.debug("Disconnecting...")
        self.client.loop_stop()
        self.client.disconnect()
