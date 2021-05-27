from enum import Enum
import random

# Define Color Enum
class Color(Enum):
    WHITE = 1
    BLACK = 2

class Daisy:
    _color = None
    _age = 0
    _albedo = None
    _max_age = 0

    def __init__(self, color, albedo, max_age):
        self._color = color
        self._albedo = albedo
        self._max_age = max_age

        # Based on NetLogo code, age is a random int between 0 to max_age
        self._age = random.randint(0, self._max_age)

    # Geter and Seter functions
    def get_age(self):
        return self._age
    
    def set_age(self, age):
        self._age = age

    def get_color(self):
        return self._color

    def get_albedo(self):
        return self._albedo
    
    def set_albedo(self, albedo):
        self._albedo = albedo

    def get_max_age(self):
        return self._max_age