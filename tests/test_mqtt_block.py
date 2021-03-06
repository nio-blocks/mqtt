import json
from unittest.mock import patch, MagicMock
import paho.mqtt.client as mqtt

from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from ..mqtt_base_block import MqttBase
from ..mqtt_publish_block import MqttPublish
from ..mqtt_subscribe_block import MqttSubscribe


class TestMqtt(NIOBlockTestCase):

    def test_mqtt_subscribe(self):
        """Block notifies proper signal when message is received"""
        blk = MqttSubscribe()
        with patch(MqttBase.__module__ + '.mqtt') as patched_mqtt:
            mock_client = MagicMock(spec=mqtt.Client)
            patched_mqtt.Client.return_value = mock_client
            self.configure_block(blk, {
                "client_config": {
                        "client_id": "clientID",
                        "topic": "mqttTopic",
                        "host": "testlocalhost",
                        "port": 0000},
                "creds": {"app_id": "dsv",
                          "access_key": "7Q2Q3Q"}
            })
            mock_client.username_pw_set.assert_called_once_with("dsv", "7Q2Q3Q")
            mock_client.connect.assert_called_once_with("testlocalhost", 0000)
            blk.start()
            mock_client.loop_start.assert_called_once_with()
            mock_client.subscribe.assert_called_once_with("mqttTopic")

            # Simulate message being received
            client = "mqttClient"
            userdata = "userData"
            message = MagicMock()
            message.topic = "mqttTopic"
            message.payload = "mqttMsg"
            mock_client.on_message(client, userdata, message)

            blk.stop()
            mock_client.loop_stop.assert_called_once_with()
            mock_client.disconnect.assert_called_once_with()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {
                "client": "mqttClient",
                "userdata": "userData",
                "payload": "mqttMsg",
                "topic": "mqttTopic",
            })

    def test_mqtt_publish(self):
        """Block publishes signals that are processed"""
        blk = MqttPublish()
        with patch(MqttBase.__module__ + '.mqtt') as patched_mqtt:
            mock_client = MagicMock(spec=mqtt.Client)
            patched_mqtt.Client.return_value = mock_client
            self.configure_block(blk, {
                "client_config": {
                        "client_id": "clientID",
                        "topic": "mqttTopic",
                        "host": "testlocalhost",
                        "port": 0000},
                "creds": {"app_id": "dsv",
                          "access_key": "7Q2Q3Q"}
            })
            mock_client.connect.assert_called_once_with("testlocalhost", 0000)
            blk.start()
            mock_client.loop_start.assert_called_once_with()

            signal_to_publish = [Signal({"test": "testt", "testtt": 1})]
            blk.process_signals(signal_to_publish)
            mock_client.publish.assert_called_once_with(
                "mqttTopic", json.dumps(signal_to_publish[0].to_dict()))

            blk.stop()
            mock_client.loop_stop.assert_called_once_with()
            mock_client.disconnect.assert_called_once_with()

    def test_mqtt_publish_custom_data(self):
        """Block publishes data based on property"""
        blk = MqttPublish()
        with patch(MqttBase.__module__ + '.mqtt') as patched_mqtt:
            mock_client = MagicMock(spec=mqtt.Client)
            patched_mqtt.Client.return_value = mock_client
            self.configure_block(blk, {
                "client_config": {
                    "client_id": "clientID",
                    "topic": "mqttTopic",
                    "host": "testlocalhost",
                    "port": 0000},
                "data": "{{ $attr }}"
            })
            blk.start()

            signal_to_publish = [Signal({"attr": "value"})]
            blk.process_signals(signal_to_publish)
            mock_client.publish.assert_called_once_with("mqttTopic", "value")
            blk.stop()
