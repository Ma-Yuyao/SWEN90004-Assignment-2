# @Time        :  2021-05-27
# @Author      :  Yuyao Ma       1111182,
#                 Chenqi Ni	    980329,
#                 Zhaochen Fan   1077663
# @Description :  This file represents daisy used for this model
 
from enum import Enum
import random

# Define Color Enum
class Color(Enum):
    WHITE = 1
    BLACK = 2

'''
This class abstracts and defines the attributes of daisy, stores information 
such as the colour, age and albedo of the daisy, 
manages the interactions between daisy and other classes  
'''
class Daisy:
    _color = None
    _age = 0
    _albedo = None
    _max_age = 0
    
    # Initialize the variables used
    def __init__(self, color, albedo, max_age):
        self._color = color
        self._albedo = albedo
        self._max_age = max_age

        # Based on NetLogo code, age is a random int between 0 to max_age
        self._age = random.randint(0, self._max_age)

    # Getter and Setter functions
    # Getter for age
    def get_age(self):
        return self._age

    # Setter for age
    def set_age(self, age):
        self._age = age

    # Getter for color
    def get_color(self):
        return self._color

    # Getter for albedo
    def get_albedo(self):
        return self._albedo

     # Setter for albedo   
    def set_albedo(self, albedo):
        self._albedo = albedo

    # Getter for albedo
    def get_max_age(self):
        return self._max_age