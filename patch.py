import math
import random

import simulator
import daisy
from daisy import Daisy, Color


class Patch(object):
    _daisy = None
    _temperature = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate_local_temperature(self):

        if self._daisy is None:
            absorbed_luminosity = ((1 - simulator.albedo_of_surface) * simulator.solar_luminosity)
        else:
            absorbed_luminosity = ((1 - self._daisy.albedo) * simulator.solar_luminosity)
        if absorbed_luminosity > 0:
            local_heating = 72 * \
                            math.log(absorbed_luminosity) + 80
        else:
            local_heating = 80
        self._temperature = ((self._temperature + local_heating) / 2)
        # return self._temperature

    def check_survivability(self):
        if self._daisy is None:
            return False
        if self._daisy.age < daisy.MAX_AGE:
            print(self._daisy.age)
            print(self._temperature)
            seed_threshold = (0.1457 * self._temperature) - (0.0032 * self._temperature * self._temperature) - 0.6443
            print(seed_threshold)
            if random.random() < seed_threshold:
                return True
            return False
        else:
            self._daisy = None
            return False
#test
class main():
    patch = Patch(1, 2)
    patch._daisy = Daisy(Color.BLACK)
    patch.calculate_local_temperature()
    print(patch._temperature)
    print(patch.check_survivability())


