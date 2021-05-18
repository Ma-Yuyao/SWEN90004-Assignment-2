import math
import random
from daisy import Daisy

class Patch(object):
    _daisy = None
    _temperature = 0
    _local_heating = 0

    # (x,y) is the coordinate of this patch in the fictionary patch_graph
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 'to calc-temperature' procedure in NetLogo code
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

    # helper function for 'to check-survivability' procedure
    def check_survivability(self):
        if self._daisy is None:
            return False
        self._daisy.set_age(self._daisy.get_age() + 1)
        if self._daisy.get_age() < self._daisy.get_max_age():
            seed_threshold = (0.1457 * self._temperature) - (0.0032 * self._temperature * self._temperature) - 0.6443
            if random.random() < seed_threshold:
                return True
            return False
        else:
            self._daisy = None
            return False

    # Geter and Seter functions
    def get_daisy(self):
        return self._daisy

    def set_daisy(self, color, albedo, max_age):
        self._daisy = Daisy(color, albedo, max_age)
    
    def set_daisy_as_None(self):
        self._daisy = None

    def get_temperature(self):
        return self._temperature
    
    def set_temperature(self, temperature):
        self._temperature = temperature
