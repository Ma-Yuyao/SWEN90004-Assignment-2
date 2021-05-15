from enum import Enum
import random

'''
WHITE_ALBEDO 和 BLACK_ALBEDO 和 MAX_AGE 应当定义在 Simulator 类中，此处仅用作测试
'''
WHITE_ALBEDO = 1
BLACK_ALBEDO = 0
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

    def __init__(self, color):
        self._color = color
        if (self._color == Color.WHITE):
            self._albedo = WHITE_ALBEDO
        elif (self._color == Color.BLACK):
            self._albedo = BLACK_ALBEDO
        '''
        根据代码，age 是一个 0 - MAX_AGE 的随机数
        '''
        self._age = random.randint(0, MAX_AGE)

    '''
    get_age 方法
    '''
    def get_age(self):
        return self._age

# Test
class main():
    daisy = Daisy(Color.WHITE)
    print(daisy.get_age())