#!/usr/bin/env python3

import Adafruit_DHT
import paho.mqtt.publish as publish
import time
import json
import logging
import config


def read_data():
    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)


def send_data(h, t):
    auth = {'username': config.LOGIN, 'password': config.PASSWORD}
    payload = json.dumps({'temperature': round(t, 1), 'humidity': round(h)})
    logging.info(payload)
    publish.single(config.TOPIC, payload, hostname=config.HOSTNAME, auth=auth)


def main():
    logging.info("dht2mqtt started")
    while True:
        h, t = read_data()
        if h > 0 and h < 100 and t > 0 and t < 100:
            try:
                send_data(h, t)
            except OSError as err:
                logging.error(
                    "couldn't contact mqtt server. Giving up till the next measurement. {}"
                    .format(err))
        else:
            logging.warning("missing or incorrect data from sensor.")
            logging.warning("t: {}, h: {}".format(t, h))
        time.sleep(config.INTERVAL)


main()
