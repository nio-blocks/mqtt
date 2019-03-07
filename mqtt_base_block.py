import paho.mqtt.client as mqtt

from nio.properties import StringProperty, IntProperty, \
                           ObjectProperty, PropertyHolder
from nio.util.discovery import not_discoverable


class AuthCreds(PropertyHolder):
    app_id = StringProperty(title="Application ID", default="", order=1)
    access_key = StringProperty(title="Access Key", default="", order=2)


class ClientConfig(PropertyHolder):
    host = StringProperty(
        title="Host", default="localhost", allow_none=False, order=1)
    port = IntProperty(
        title="Port", default=1883, allow_none=False, order=2)
    topic = StringProperty(
        title="Topic", default="", allow_none=True, order=3)


@not_discoverable
class MqttBase(object):

    client_config = ObjectProperty(
        ClientConfig,
        title="MQTT Client Config",
        default=ClientConfig(),
        order=1,
    )
    creds = ObjectProperty(
        AuthCreds,
        title="Authorization Creds",
        default=AuthCreds(),
        advanced=True,
        order=2,
    )

    def __init__(self):
        super().__init__()
        self._client = None

    def configure(self, context):
        super().configure(context)
        self._client = mqtt.Client()
        self._connect()

    def stop(self):
        self._disconnect()
        super().stop()

    def _connect(self):
        self.logger.info("Connecting...")
        self._client.on_connect = self._on_connect
        app_id = self.creds().app_id()
        app_key = self.creds().access_key()
        if app_id or app_key:
            self._client.username_pw_set(app_id, app_key)
        self._client.connect(self.client_config().host(),
                             self.client_config().port())
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        self.logger.info("Connected with result code {}".format(rc))

    def _disconnect(self):
        self.logger.info("Disconnecting...")
        self._client.loop_stop()
        self._client.disconnect()
