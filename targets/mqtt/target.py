import paho.mqtt.client as mqtt

import json
import logging


class Target():
    def __init__(self):
        ""

    def on_connect(self, client, userdata, flags, rc):
        logging.debug("MQTT Connected with result code " + str(rc))

    def on_message(self, client, userdata, msg):
        logging.debug(msg.topic + " " + str(msg.payload))

    def send(self, data):
        payload = json.dumps(data)
        logging.debug("send payload: {}".format(payload))
        self.client.connect(self.host, self.port)
        self.client.publish(self.topic, data)
        self.client.disconnect()

    def setup(self, params):
        self.host = params['mqtt']['host']
        self.port = params['mqtt']['port'] if 'port' in params['mqtt'] else 1883
        self.topic = params['mqtt']['topic']
        self.auth = {
            'username': params['mqtt']['user'],
            'password': params['mqtt']['pass']
        }
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
