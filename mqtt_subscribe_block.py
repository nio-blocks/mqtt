from nio import GeneratorBlock
from nio.properties import VersionProperty
from nio.signal.base import Signal

from .mqtt_base_block import MqttBase


class MqttSubscribe(MqttBase, GeneratorBlock):

    version = VersionProperty('0.1.0')

    def configure(self, context):
        super().configure(context)
        self._client.on_message = self._on_message

    def start(self):
        super().start()
        self._client.subscribe(self.client_config().topic())

    def _on_message(self, client, userdata, message):
        self.logger.debug("Received message from client '{}' on topic '{}'. "
                          "{}".format(client, message.topic, message.payload))
        self.notify_signals([Signal({"client": client,
                                     "userdata": userdata,
                                     "payload": message.payload,
                                     "topic": message.topic})])

    def stop(self):
        self._client.unsubscribe(self.client_config().topic())
        super().stop()
