from nio.properties import VersionProperty
from nio.util.discovery import discoverable
from nio.signal.base import Signal

from .mqtt_base_block import MqttBase


@discoverable
class MqttSubscribe(MqttBase):

    version = VersionProperty('0.1.0')

    def configure(self, context):
        super().configure(context)
        self.client.subscribe(self.topic())
        self.client.on_message = self.on_message

    def on_message(self, client, userdata, message):
        self.logger.debug("Received message from client '{}' on topic '{}'. "
                          "{}".format(client, message.topic, message.payload))
        self.notify_signals([Signal({"client": client,
                                     "userdata": userdata,
                                     "payload": message.payload,
                                     "topic": message.topic})])


    def stop(self):
        self.client.unsubscribe(self.topic())
        super().stop()