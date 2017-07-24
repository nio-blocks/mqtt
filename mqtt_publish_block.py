from nio.properties import VersionProperty
from nio.util.discovery import discoverable

from .mqtt_base_block import MqttBase


@discoverable
class MqttPublish(MqttBase):

    version = VersionProperty('1.0.0')
    # Create propert for mesage to send?

    def process_signals(self, signals):
        for signal in signals:
            self.logger.debug("Publishing signal to topic '{}': {}"
                              .format(self.topic(), signal.to_dict()))
            self.client.publish(self.topic(), signal.to_dict())

# single vs multiple publish?
