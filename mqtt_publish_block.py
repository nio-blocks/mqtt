from nio import TerminatorBlock
from nio.properties import VersionProperty, Property

from .mqtt_base_block import MqttBase


class MqttPublish(MqttBase, TerminatorBlock):

    version = VersionProperty("0.2.0")
    data = Property(
        title="Data to Publish",
        default="{{ json.dumps($.to_dict()) }}",
        order=0,
    )

    def process_signal(self, signal, input_id=None):
        data = self.data(signal)
        topic = self.client_config().topic()
        self.logger.debug("Publishing {} to topic '{}'".format(data, topic))
        self._client.publish(topic, data)
