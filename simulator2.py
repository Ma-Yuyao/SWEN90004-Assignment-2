from enum import Enum
import random

'''
WHITE_ALBEDO 和 BLACK_ALBEDO 和 MAX_AGE, 从Daisy里拿的
'''
WHITE_ALBEDO = 1
BLACK_ALBEDO = 0
MAX_AGE = 25

'''
定义 SCENARIO 枚举
'''
class Scenario(Enum):
    #RAMP-UP-RAMP-DOWN
    RURD = 1
    #LOW SOLAR LUMINOSITY
    LSL = 2
    #HIGH SOLAR LUMINOSITY
    HSL = 3
    #OUR SOLAR LUMINOSITY
    OSL = 4
#scenario_phase和scenario是一个东西吗
SCENARIO_PHASE

'''
constants from the model
'''
START-RATIO-WHITE
START-RATIO-BLACK
ALBEDO_OF_SURFACE
#(constants used to calculate seed-threshold)
SEED_THRESHOLD_CONSTANT_1 = 0.1457
SEED_THRESHOLD_CONSTANT_2 = 0.0032
SEED_THRESHOLD_CONSTANT_3 = 0.6443
MAX_PATCH_SIZE

#会变化的variable
solar_luminosity 
#mean temperature of patches
global_temperature = 

#timer, used to monitor the modeling process
TICK = 0
#diffuse of heat, according to the original model
DIFFUSE = 0.5
Map [(x,y), Patch]

class Simulator(object):

    def __init__(self,scenario,albedo_of_surface,\
                 start-ratio-white,start-ratio-black,\
                 albedo_of_surface,white_albedo,black_albedo\
                 ):

        #设置不会变化的常量
        self.START-RATIO-WHITE = start-ratio-white
        self.START-RATIO-BLACK = start-ratio-black
        self.WHITE_ALBEDO = white_albedo
        self.BLACK_ALBEDO = black_albedo
        #~~~~~~~~~~问题:~~~~~~~~~~~~~~~
        #Albeo of surface要随着雏菊的比例变化而改变吗?
        #原代码里只有calc-temperature里提到了一下,用来set absorbed-luminosity
        self.ALBEDO_OF_SURFACE = albedo_of_surface

        #检查scenario设置luminosity
        '''
        ~~~~~~~~~~问题:~~~~~~~~~~~~~~~
        源代码里to go下面end前又设置了一遍这个是什么意思
        '''
        if (scenario == Scenario.RURD):
            self.solar_luminosity = 0.8
        elif (scenario == Scenario.LSL):
            self.solar_luminosity = 0.6
        elif (scenario == Scenario.HSL):
            self.solar_luminosity = 1.4
        elif (scenario == Scenario.OSL):
            self.solar_luminosity = 1.0

    def update(self):
        TICK += 1

        '''
        如果是RURD的话就更新solar_luminosity
        '''
        if (scenario == Scenario.RURD):
        if ticks > 200 and ticks <= 400：
            solar_luminosity = format( (solar_luminosity + 0.005), '.4f')
            # ~~~~~~~~~~问题:~~~~~~~~~~~~~~~
            #下面的precision和 4什么意思? 取小数点后四位?
            #set solar-luminosity precision (solar-luminosity + 0.005) 4
        if ticks > 600 and ticks <= 850:
            solar_luminosity = format( (solar_luminosity - 0.0025), '.4f')
            # ~~~~~~~~~~问题:~~~~~~~~~~~~~~~
            # 同上
            set solar-luminosity precision (solar-luminosity - 0.0025) 4
        ]

class main():
