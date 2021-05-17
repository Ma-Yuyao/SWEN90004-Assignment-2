import argparse
import random

import numpy

# from pandas import np
from daisy import Color, Daisy
from patch import Patch

MIN_XCOR = 0
MAX_XCOR = 28
MIN_YCOR = 0
MAX_YCOR = 28

# {(x,y):patch}
patch_graph = {}


def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_whites", help="white num", type=int, nargs='?', const=1, default=20,
                        choices=range(0, 50))
    parser.add_argument("--start_blacks", help="black num", type=int, nargs='?', const=1, default=20,
                        choices=range(0, 50))
    parser.add_argument("--albedo_whites", help="albedo of whites", type=float, nargs='?', const=1, default=0.75,
                        choices=numpy.arange(0, 1, 0.01))
    parser.add_argument("--albedo_blacks", help="albedo of blacks", type=float, nargs='?', const=1, default=0.25,
                        choices=numpy.arange(0, 1, 0.01))
    parser.add_argument("--scenario", help="scenario", nargs='?', const=1, default="ramp-up-ramp-down",
                        choices=["ramp-up-ramp-down", "low-solar-luminosity", "our-solar-luminosity",
                                 "high-solar-luminosity"])
    parser.add_argument("--solar_luminosity", help="albedo of surface", type=float, nargs='?', const=1, default=0.800,
                        choices=numpy.arange(0.000, 3.000, 0.001))
    parser.add_argument("--albedo_of_surface", help="albedo of surface", type=float, nargs='?', const=1, default=0.4,
                        choices=numpy.arange(0, 1, 0.01))
    args = parser.parse_args()

    return args


# def output():


#
class Simulator(object):

    def __init__(self, args):
        self.start_whites = args.start_whites
        self.start_blacks = args.start_blacks
        self.albedo_whites = args.albedo_whites
        self.albedo_blacks = args.albedo_blacks
        self.albedo_of_surface = args.albedo_of_surface
        self.scenario = args.scenario
        self.solar_luminosity = args.solar_luminosity
        self.DIFFUSE_PERCENT = 50

    def set_up_patch_graph(self):
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = Patch(x, y)
                patch_graph[pos] = patch

    def get_patch_list(self):
        patch_list = []
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                patch_list.append(patch)
        return patch_list

    # get patch in random and remove it from patchList

    def get_random_patch(self, patch_list):
        list_len = len(patch_list)
        if list_len == 0:
            return None
        rand_index = random.randint(0, list_len-1)
        rand_patch = patch_list[rand_index]
        del patch_list[rand_index]
        return rand_patch, patch_list

    def get_neighbors(self, x, y):
        neighbor_list = [i for i in range(8)]
        # up_neighbor
        neighbor_list[0] = (str(x) + "," + str(y + 1)) if y + 1 < MAX_YCOR else None
        # down_neighbor
        neighbor_list[1] = (str(x) + "," + str(y - 1)) if y - 1 > MIN_YCOR else None
        # left_neighbor
        neighbor_list[2] = (str(x - 1) + "," + str(y)) if x - 1 > MIN_XCOR else None
        # right_neighbor
        neighbor_list[3] = (str(x + 1) + "," + str(y)) if x + 1 < MAX_XCOR else None
        # left up neighbor
        neighbor_list[4] = (str(x - 1) + "," + str(y + 1)) if x - 1 > MIN_XCOR and y + 1 < MAX_YCOR else None
        # left down neighbor
        neighbor_list[5] = (str(x - 1) + "," + str(y - 1)) if x - 1 > MIN_XCOR and y - 1 > MIN_YCOR else None
        # right up neighbor
        neighbor_list[6] = (str(x + 1) + "," + str(y + 1)) if x + 1 < MAX_XCOR and y + 1 < MAX_YCOR else None
        # right down neighbor
        neighbor_list[7] = (str(x + 1) + "," + str(y - 1)) if x + 1 < MAX_XCOR and y - 1 > MIN_YCOR else None
        return neighbor_list

    def check_survivability_handler(self):
        patch_list = self.get_patch_list()
        num = len(patch_list)
        for i in range(0, num):
            rand_patch, patch_list = self.get_random_patch(patch_list)
            if rand_patch is None:
                return
            # seed a same type daisy if true
            if rand_patch.check_survivability():
                # print (rand_patch.get_daisy())
                neighbors_pos_list = []
                neighbors_pos = self.get_neighbors(rand_patch.x, rand_patch.y)
                # print (neighbors_pos)
                for j in range(0, len(neighbors_pos)-1):
                    if (neighbors_pos[j] != None):
                        neighbors_pos_list.append(neighbors_pos[j])
                # print (neighbors_pos_list)
                while True:
                    if len(neighbors_pos_list) == 0: break
                    rand_index = random.randint(0, len(neighbors_pos_list)-1)
                    neighbor_pos = neighbors_pos_list[rand_index]
                    del neighbors_pos_list[rand_index]
                    neighbor = patch_graph[neighbor_pos]
                   
                    # if neighbor.get_daisy() is None:
                    #     neighbor.set_daisy(rand_patch.get_daisy().get_color())
                    #     break
    
    '''
    deal with diffuse. to finish the function of diffuse in NetLogo
    equal: diffuse temperature .5
    '''
    def diffuseHandler(self):
        # calculate how much the patch lose and receive
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                diffuse_unit = patch.get_temperature() * self.DIFFUSE_PERCENT / 100 / 8
                patch.set_temperature( patch.get_temperature() * (100 - self.DIFFUSE_PERCENT) / 100)
                for neighbour_pos in self.get_neighbors(x,y):
                    if (neighbour_pos == None):
                        continue
                    diffused_patch = patch_graph[neighbour_pos]
                    diffused_patch.set_receiced_diffuse(diffused_patch.get_receiced_diffuse() + diffuse_unit)
        
        # # update the lose and received temperature.
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                patch.set_temperature(patch.get_temperature() + patch.get_receiced_diffuse())
                patch.set_receiced_diffuse(0)

    def get_empty_patch_list(self):
        empty_patch_list = []
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                if patch.get_daisy() is None:
                    empty_patch_list.append(patch)
        return empty_patch_list

    def seed_daisies_randomly(self):
        empty_patch_list = self.get_empty_patch_list()
        # print(empty_patch_list)
        total_patch = (MAX_XCOR - MIN_XCOR + 1) * (MAX_YCOR - MIN_YCOR + 1)
        white_daisies_num = round(total_patch * self.start_whites / 100)
        black_daisies_num = round(total_patch * self.start_blacks / 100)
        for white_count in range(1, white_daisies_num):
            empty_patch, empty_patch_list = self.get_random_patch(empty_patch_list)
            if empty_patch != None:
                empty_patch.set_daisy(Color.WHITE)
                patch_graph[empty_patch.x, empty_patch.y] = empty_patch
        for black_count in range(1, white_daisies_num):
            empty_patch, empty_patch_list = self.get_random_patch(empty_patch_list)
            if empty_patch != None:
                empty_patch.set_daisy(Color.BLACK)
                patch_graph[empty_patch.x, empty_patch.y] = empty_patch

    def calc_temperature(self):
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                patch.calculate_local_temperature(self.albedo_of_surface, self.solar_luminosity)

    def initialize(self):
        self.set_up_patch_graph()
        self.seed_daisies_randomly()
        # ask patches [calc-temperature]
        self.calc_temperature()
        


    def test(self):
        self.initialize()
        # self.set_up_patch_graph()
        self.check_survivability_handler()
        self.diffuseHandler()
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                if patch.get_daisy() != None:
                    print(patch.get_temperature())

if __name__ == "__main__":
    daisy_world = Simulator(get_input())
    daisy_world.test()
