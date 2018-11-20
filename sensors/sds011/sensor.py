#!/usr/bin/env python3
# based on: Dr. M. Luetzelberger sds011_pylab.py

import serial
import struct
import time
import sys
import logging


class Sensor():
    def __init__(self):
        ""

    def sensor_wake(self):
        cmd = b"\xaa\xb4\x06\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x05\xab"
        self.ser.write(cmd)

    def sensor_sleep(self):
        cmd = b"\xaa\xb4\x06\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\x05\xab"
        self.ser.write(cmd)

    def process_frame(self, d):
        r = struct.unpack('<HHxxBBB', bytes(d[2:]))
        pm25 = round(r[0] / 10.0, 1)
        pm10 = round(r[1] / 10.0, 1)
        return {'PM25': pm25, 'PM10': pm10}

    def console_read(self):
        byte = 0
        while byte != b"\xaa":
            byte = self.ser.read(size=1)
            d = self.ser.read(size=10)
            if d[0] == 192:
                return self.process_frame(byte + d)

    def sensor_live(self, params):
        """in case you want to invoke this module from console"""
        self.sensor_wake()
        while True:
            self.sensor_wake()
            time.sleep(params['spinup_wait'])
            pm = self.console_read()
            print("pm2.5: {pm25}, pm10: {pm10}".format(**pm))
            print("time to sleep for {} seconds.".format(30))
            self.sensor_sleep()
            time.sleep(30)

    def setup(self, params):
        self.ser = serial.Serial()
        self.ser.port = params['serial_port']
        self.ser.baudrate = params[
            'baudrate'] if 'baudrate' in params else 9600
        self.ser.open()
        self.ser.flushInput()
        self.sensor_sleep()  # just to be sure
        self.SPINUP_WAIT = params[
            'spinup_wait'] if 'spinup_wait' in params else 5

    def read(self):
        self.sensor_wake()
        time.sleep(self.SPINUP_WAIT)
        pm = self.console_read()
        self.sensor_sleep()
        return pm


if __name__ == "__main__":
    # TODO: fix
    S = Sensor(sys.argv[1])
    S.sensor_wake()
    try:
        S.sensor_live({'add_params_here'})
    except KeyboardInterrupt:
        S.sensor_sleep()
