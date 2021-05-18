from enum import Enum
import random

'''
WHITE_ALBEDO 和 BLACK_ALBEDO 和 MAX_AGE 应当定义在 Simulator 类中，此处仅用作测试
'''
# WHITE_ALBEDO = 0.75
# BLACK_ALBEDO = 0.25
MAX_AGE = 25

'''
定义 Color 枚举
'''


class Color(Enum):
    WHITE = 1
    BLACK = 2

class Daisy:
    _color = None
    _age = 0
    _albedo = None

    def __init__(self, color, albedo):
        self._color = color
        self._albedo = albedo
        '''
        根据代码，age 是一个 0 - MAX_AGE 的随机数
        '''
        self._age = random.randint(0, MAX_AGE)

    '''
    get_age 方法
    '''

    def get_age(self):
        return self._age

    def get_color(self):
        return self._color

    def get_albedo(self):
        return self._albedo
    
    def set_albedo(self, albedo):
        self._albedo = albedo

    def set_age(self, age):
        self._age = age



# Test
# class main():
#     daisy = Daisy(Color.WHITE)
#     print(daisy.get_age())
