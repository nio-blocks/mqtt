import paho.mqtt.client as mqtt

from nio.properties import StringProperty, IntProperty, \
                           ObjectProperty, PropertyHolder
from nio.util.discovery import not_discoverable


class AuthCreds(PropertyHolder):
    app_id = StringProperty(title="Application ID", default="")
    access_key = StringProperty(title="Access Key", default="")


class ClientConfig(PropertyHolder):
    client_id = StringProperty(title="Client ID", default="", allow_none=False)
    port = IntProperty(title="Port", default=1883, allow_none=False)
    host = StringProperty(title="Host", default="localhost", allow_none=False)
    topic = StringProperty(title="Topic", default="", allow_none=True)


@not_discoverable
class MqttBase(object):

    client_config = ObjectProperty(ClientConfig,
                           title="MQTT Client Config", default=ClientConfig())
    creds = ObjectProperty(AuthCreds,
                           title="Authorization Creds", default=AuthCreds())

    def __init__(self):
        super().__init__()
        self._client = None

    def configure(self, context):
        super().configure(context)
        self._client = mqtt.Client(self.client_config().client_id())
        self._connect()

    def stop(self):
        self._disconnect()
        super().stop()

    def _connect(self):
        self.logger.debug("Connecting...")
        self._client.on_connect = self._on_connect
        self._client.username_pw_set(self.creds().app_id(),
                                     self.creds().access_key())
        self._client.connect(self.client_config().host(),
                             self.client_config().port())
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        self.logger.debug("Connected with result code {}".format(
            str(rc)))

    def _disconnect(self):
        self.logger.debug("Disconnecting...")
        self._client.loop_stop()
        self._client.disconnect()
