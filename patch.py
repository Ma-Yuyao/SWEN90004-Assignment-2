import math
import random

import daisy
from daisy import Daisy, Color


class Patch(object):
    _daisy = None
    _temperature = 0
    _receiced_diffuse = 0
    _local_heating = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def calculate_local_temperature(self, albedo_of_surface, solar_luminosity):

        if self._daisy is None:
            absorbed_luminosity = ((1 - albedo_of_surface) * solar_luminosity)
        else:
            absorbed_luminosity = ((1 - self._daisy.get_albedo()) * solar_luminosity)
        if absorbed_luminosity > 0:
            self._local_heating = 72 * math.log(absorbed_luminosity) + 80
        else:
            self._local_heating = 80
        self._temperature = ((self._temperature + self._local_heating) / 2)
        # return self._temperature

    def check_survivability(self):
        if self._daisy is None:
            return False
        self._daisy.set_age(self._daisy.get_age() + 1)
        if self._daisy.get_age() < daisy.MAX_AGE:
            # print(self._daisy.get_age())
            # print(self._temperature)
            seed_threshold = (0.1457 * self._temperature) - (0.0032 * self._temperature * self._temperature) - 0.6443
            if random.random() < seed_threshold:
                return True
            return False
        else:
            self._daisy = None
            return False

    def get_daisy(self):
        return self._daisy

    def set_daisy(self, color, albedo):
        self._daisy = Daisy(color, albedo)

    
    def get_temperature(self):
        return self._temperature
    
    def set_temperature(self, temperature):
        self._temperature = temperature

    def get_receiced_diffuse(self):
        return self._receiced_diffuse
    
    def set_receiced_diffuse(self, receiced_diffuse):
        self._receiced_diffuse = receiced_diffuse
    
    def get_local_heating(self):
        return self._local_heating


# test
# class main():
#     patch = Patch(1, 2)
#     patch._daisy = Daisy(Color.BLACK)
#     patch.calculate_local_temperature(1, 2)
#     print(patch.temperature)
#     print(patch.check_survivability())
