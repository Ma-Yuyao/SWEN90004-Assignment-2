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
    __color = None
    __age = 0
    __albedo = None

    def __init__(self, color):
        self.__color = color
        if (self.__color == Color.WHITE):
            self.__albedo = WHITE_ALBEDO
        elif (self.__color == Color.BLACK):
            self.__albedo = BLACK_ALBEDO
        '''
        根据代码，age 是一个 0 - MAX_AGE 的随机数
        '''
        self.__age = random.randint(0, MAX_AGE)

    '''
    get_age 方法
    '''
    def get_age(self):
        return self.__age

# Test
class main():
    daisy = Daisy(Color.WHITE)
    print(daisy.get_age())