import logging
import json
import requests


class Sensor():
    def __init__(self):
        ""

    def setup(self, params):
        self.uri_params = dict((k, params[k]) for k in ('lat', 'lng'))
        self.headers = {
            'Accept': 'application/json',
            'apikey': params['apikey']
        }
        self.uri = "https://airapi.airly.eu/v2/measurements/point"

    def read(self):
        r = requests.get(
            self.uri, params=self.uri_params, headers=self.headers)
        try:
            resp = r.json()
        except ValueError:
            logging.error("Invalid json: {}".format(r.text))
        values = json.loads(r.text)['current']['values']
        readings = {}
        for v in values:
            readings[v['name']] = v['value']
        return readings
