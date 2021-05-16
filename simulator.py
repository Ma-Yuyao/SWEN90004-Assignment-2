import argparse
import random

import numpy

# from pandas import np
from daisy import Daisy
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
        self.star_blacks = args.start_blacks
        self.albedo_whites = args.albedo_whites
        self.albedo_blacks = args.albedo_blacks
        self.albedo_of_surface = args.albedo_of_surface
        self.scenario = args.scenario
        self.solar_luminosity = args.solar_luminosity

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
        return rand_patch

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
            rand_patch = self.get_random_patch(patch_list)
            if rand_patch is None:
                return
            # seed a same type daisy if true
            if rand_patch.check_survivability:
                neighbors_pos_list = []
                neighbors_pos = self.get_neighbors(rand_patch.x, rand_patch.y)
                for j in range(0, len(neighbors_pos_list)):
                    neighbors_pos_list.append(neighbors_pos[j])
                while True:
                    if len(neighbors_pos_list) == 0: break
                    rand_index = random.randint(0, len(neighbors_pos_list))
                    neighbor_pos = neighbors_pos_list[rand_index]
                    del neighbors_pos_list[rand_index]
                    neighbor = patch_graph[neighbor_pos]
                    if neighbor.get_daisy() is None:
                        neighbor.set_daisy(rand_patch.get_daisy().get_color())
                        break

    def test(self):

        self.set_up_patch_graph()

        self.check_survivability_handler()
        print(patch_graph)


if __name__ == "__main__":
    daisy_world = Simulator(get_input())
    daisy_world.test()
