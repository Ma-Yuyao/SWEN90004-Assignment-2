'''
This class is the entry point for the project to start up the simulation. 
'''

from daisy_world import *

def main():
    daisy_world_simulator = daisy_world(get_input())
    daisy_world_simulator.start_simulation()

if __name__ == "__main__":
    main()