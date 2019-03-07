MqttPublish
===========
Publish messages with the MQTT protocol.

Properties
----------
- **Data to Publish** - The data to publish to the MQTT channel. Defaults to a JSON representation of the incoming signal
- **MQTT Client Config**
	- **Host** - The MQTT server's host
	- **Port** - The MQTT server's port
	- **Topic** - The topic to publish to (string)
- **Authorization Creds** - optional MQTT authentication
	- **Application ID** - The application ID or username to authenticate with
	- **Access Key** - The access key or password to authenticate with

Inputs
------
- **default**: List of signals containing the data to be published.
