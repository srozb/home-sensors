#!/usr/bin/env python3

import logging
import sys
import yaml
import importlib
import time


def read_yaml():
    params_file = sys.argv[1] if len(sys.argv) == 2 else "default.yaml"
    with open(params_file, 'r') as f:
        return yaml.safe_load(f.read())


def setup_sensor(sensor_params):
    sensor_module = importlib.import_module("sensors." + sensor_params['type'],
                                            "sensor")
    Sensor = sensor_module.Sensor()
    Sensor.setup(sensor_params)
    logging.info("Sensor {} ({}) configured.".format(sensor_params['name'],
                                                     sensor_params['type']))
    return Sensor


def setup_target(target_params):
    target_module = importlib.import_module(
        "targets." + list(target_params.keys())[0], "target")
    Target = target_module.Target()
    Target.setup(target_params)
    logging.info("Target {} configured.".format(list(target_params.keys())[0]))
    return Target


def daemon_init():
    params = read_yaml()
    logging.basicConfig(level=params['logging']['level'])
    return params


def daemon_run(Sensor, Target, interval):
    logging.info("entering pooling loop.")
    while True:
        Target.send(Sensor.read())
        time.sleep(interval)
        logging.debug("waiting for {} secs.".format(interval))


def main():
    params = daemon_init()
    Sensor = setup_sensor(params['sensor'])
    Target = setup_target(params['target'])
    daemon_run(Sensor, Target, params['sensor']['interval'])


main()
