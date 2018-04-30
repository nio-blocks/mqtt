import paho.mqtt.client as mqtt

from nio.properties import StringProperty, IntProperty
from nio.util.discovery import not_discoverable


@not_discoverable
class MqttBase(object):

    client_id = StringProperty(title="Client ID", default="", allow_none=False)
    port = IntProperty(title="Port", default=1883, allow_none=False)
    host = StringProperty(title="Host", default="localhost", allow_none=False)
    topic = StringProperty(title="Topic", default="", allow_none=True)
    app_id = StringProperty(title="Application ID", default="")
    access_key = StringProperty(title="Access Key", default="")

    def __init__(self):
        super().__init__()
        self._client = None

    def configure(self, context):
        super().configure(context)
        self._client = mqtt.Client(self.client_id())
        self._connect()

    def stop(self):
        self._disconnect()
        super().stop()

    def _connect(self):
        self.logger.debug("Connecting...")
        self._client.on_connect = self._on_connect
        self._client.username_pw_set(self.app_id(), self.access_key())
        self._client.connect(self.host(), self.port())
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        self.logger.debug("Connected with result code {}".format(
            str(rc)))

    def _disconnect(self):
        self.logger.debug("Disconnecting...")
        self._client.loop_stop()
        self._client.disconnect()
