from nio import TerminatorBlock
from nio.properties import VersionProperty

from .mqtt_base_block import MqttBase


class MqttPublish(MqttBase, TerminatorBlock):

    version = VersionProperty("0.1.0")

    def process_signals(self, signals):
        for signal in signals:
            self.logger.debug("Publishing signal to topic '{}': {}"
                              .format(self.client_config().topic(), signal.to_dict()))
            self._client.publish(self.client_config().topic(), signal.to_dict())
