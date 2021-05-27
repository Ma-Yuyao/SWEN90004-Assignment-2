# @Time        :  2021-05-27
# @Author      :  Yuyao Ma       1111182,
#                 Chenqi Ni	    980329,
#                 Zhaochen Fan   1077663
# @Description :  This file is the entry point for the project to start up 
#                 the simulation.

'''
This class is the entry point for the project to start up the simulation. 
'''

from daisy_world import *

# Entry function for lauching this project
def main():
    daisy_world_simulator = daisy_world(get_input())
    daisy_world_simulator.start_simulation()

if __name__ == "__main__":
    main()