#!/usr/bin/env python3

import Adafruit_DHT
import logging


class Sensor():
    def __init__(self):
        ""

    def setup(self, params):
        self.PORT = params['port']

    def read(self):
        logging.debug("read")
        h, t = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, self.PORT)
        readings = {'temperature': round(t, 1), 'humidity': round(h)}
        logging.debug(readings)
        return readings