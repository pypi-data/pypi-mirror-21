"""
Copyright (c) 2015-2017 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import time

import requests

from . import exceptions

# The switch uses a different schema than the bulbs and the buttons.
URI = 'api/v1/device'


class MyStromPlug(object):
    """A class for a myStrom switch."""

    def __init__(self, host):
        """Initialize the switch."""
        self.resource = 'http://{}'.format(host)
        self.timeout = 5
        self.data = None
        self.state = None
        self.consumption = 0

    def set_relay_on(self):
        """Turn the relay on."""
        if not self.get_relay_state():
            try:
                request = requests.get(
                    '{}/relay'.format(self.resource), params={'state': '1'},
                    timeout=self.timeout)
                if request.status_code == 200:
                    self.data['relay'] = True
            except requests.exceptions.ConnectionError:
                raise exceptions.MyStromConnectionError()

    def set_relay_off(self):
        """Turn the relay off."""
        if self.get_relay_state():
            try:
                request = requests.get(
                    '{}/relay'.format(self.resource), params={'state': '0'},
                    timeout=self.timeout)
                if request.status_code == 200:
                    self.data['relay'] = False
            except requests.exceptions.ConnectionError:
                raise exceptions.MyStromConnectionError()

    def get_status(self):
        """Get the details from the switch."""
        try:
            request = requests.get(
                '{}/report'.format(self.resource), timeout=self.timeout)
            self.data = request.json()
            return self.data
        except (requests.exceptions.ConnectionError, ValueError):
            raise exceptions.MyStromConnectionError()

    def get_relay_state(self):
        """Get the relay state."""
        self.get_status()
        try:
            self.state = self.data['relay']
        except TypeError:
            self.state = False

        return bool(self.state)

    def get_consumption(self):
        """Get current power consumption in mWh."""
        self.get_status()
        try:
            self.consumption = self.data['power']
        except TypeError:
            self.consumption = 0

        return self.consumption

class MyStromBulb(object):
    """A class for a myStrom bulb."""

    def __init__(self, host, mac):
        """Initialize the bulb."""
        self.resource = 'http://{}'.format(host)
        self._mac = mac
        self.timeout = 5
        self.data = None
        self.state = None
        self.consumption = 0
        self.color = None
        self.transition_time = 0

    def get_status(self):
        """Get the details from the bulb."""
        try:
            request = requests.get(
                '{}/{}/'.format(self.resource, URI), timeout=self.timeout)
            self.raw_data = request.json()
            # Doesn't always work !!!!!
            #self._mac = next(iter(self.raw_data.keys()))
            self.data = self.raw_data[self._mac]
            return self.data
        except (requests.exceptions.ConnectionError, ValueError):
            raise exceptions.MyStromConnectionError()

    def get_bulb_state(self):
        """Get the relay state."""
        self.get_status()
        try:
            self.state = self.data['on']
        except TypeError:
            self.state = False

        return bool(self.state)

    def get_power(self):
        """Get current power."""
        self.get_status()
        try:
            self.consumption = self.data['power']
        except TypeError:
            self.consumption = 0

        return self.consumption

    def get_transition_time(self):
        """Get the transition time in ms."""
        self.get_status()
        try:
            self.transition_time = self.data['ramp']
        except TypeError:
            self.transition_time = 0

        return self.transition_time

    def get_color(self):
        """Get current color."""
        self.get_status()
        try:
            self.color = self.data['color']
            self.mode = self.data['mode']
        except TypeError:
            self.color = 0
            self.mode = ''

        return {'color': self.color, 'mode': self.mode}

    def set_color_hex(self, value):
        """Turn the bulb on with the given color as HEX.

        white: FF000000
        red:   00FF0000
        green: 0000FF00
        blue:  000000FF
        """
        try:
            request = requests.post(
                '{}/{}/{}/'.format(self.resource, URI, self._mac),
                data={
                    'action': 'on',
                    'mode': 'rgb',
                    'color': value,
                },
                timeout=self.timeout)
            if request.status_code == 200:
                pass
        except requests.exceptions.ConnectionError:
            raise exceptions.MyStromConnectionError()

    def set_color_hsv(self, hue, saturation, value):
        """Turn the bulb on with the given values as HSV."""
        try:
            # 'color': "12;100;100" -> JSON? 'color': [12, 100, 100]
            # urlencoding issue
            import subprocess
            subprocess.run(
                [
                    'curl', '-d', 'action=on', '-d', 'mode=hsv', '-d',
                    'color={};{};{}'.format(hue, saturation, value),
                    '{}/{}/{}'.format(self.resource, URI, self._mac),
                 ],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # request = requests.post(
            #     '{}/{}/{}'.format(self.resource, URI, self._mac),
            #     data={
            #         'action': 'on',
            #         'mode': 'hsv',
            #         'color': '{};{};{}'.format(hue, saturation, value),
            #     },
            #     timeout=self.timeout)
            # if request.status_code == 200:
            #     self.data['on'] = True
        except requests.exceptions.ConnectionError:
            raise exceptions.MyStromConnectionError()

    def set_white(self):
        """Turn the bulb on, full white."""
        self.set_color_hex('FF000000')

    def set_rainbow(self, duration):
        """Turn the bulb on, create a rainbow."""
        self.set_transition_time(100)
        for i in range(0, 359):
            self.set_color_hsv(i, 100, 100)
            time.sleep(duration/359)

    def set_sunrise(self, duration):
        """Turn the bulb on, full white."""
        self.set_transition_time(duration/100)
        for i in range(0, duration):
            try:
                import subprocess
                subprocess.run(
                    [
                        'curl', '-d', 'action=on', '-d', 'mode=mono', '-d',
                        'color=3;{}'.format(i),
                        '{}/{}/{}'.format(self.resource, URI, self._mac),
                     ],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except requests.exceptions.ConnectionError:
                raise exceptions.MyStromConnectionError()
            time.sleep(duration/100)

    def set_flashing(self, duration, color1, color2):
        """Turn the bulb on, full white."""
        self.set_transition_time(100)
        for i in range(0, int(duration/2)):
            self.set_color_hex(color1)
            time.sleep(1)
            self.set_color_hex(color2)
            time.sleep(1)

    def set_transition_time(self, value):
        """Set the transition time in ms."""
        try:
            request = requests.post(
                '{}/{}/{}/'.format(self.resource, URI, self._mac),
                data={
                    'ramp': value,
                },
                timeout=self.timeout)
            if request.status_code == 200:
                pass
        except requests.exceptions.ConnectionError:
            raise exceptions.MyStromConnectionError()

    def set_off(self):
        """Turn the bulb off."""
        try:
            request = requests.post(
                '{}/{}/{}/'.format(self.resource, URI, self._mac),
                data={
                    'action': 'off',
                },
                timeout=self.timeout)
            if request.status_code == 200:
                pass
        except requests.exceptions.ConnectionError:
            raise exceptions.MyStromConnectionError()
