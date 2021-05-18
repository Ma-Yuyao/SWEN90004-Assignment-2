import argparse
import random

# import numpy

# from pandas import np
from daisy import Color, Daisy
from patch import Patch

MIN_XCOR = 0
MAX_XCOR = 29
MIN_YCOR = 0
MAX_YCOR = 29

# {(x,y):patch}
patch_graph = {}

def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticks", help="total ticks, Default: Infinite", type=float, nargs='?', const=1, default=float('inf'))
    parser.add_argument("--start_whites", help="white num", type=int, nargs='?', const=1, default=20,
                        choices=range(0, 50))
    parser.add_argument("--start_blacks", help="black num", type=int, nargs='?', const=1, default=20,
                        choices=range(0, 50))
    parser.add_argument("--albedo_whites", help="albedo of whites", type=float, nargs='?', const=1, default=0.75)
    parser.add_argument("--albedo_blacks", help="albedo of blacks", type=float, nargs='?', const=1, default=0.25)
    parser.add_argument("--scenario", help="scenario", nargs='?', const=1, default="main-cuurent-luminosity",
                        choices=["ramp-up-ramp-down", "low-solar-luminosity", "our-solar-luminosity",
                                 "high-solar-luminosity"])
    parser.add_argument("--solar_luminosity", help="albedo of surface", type=float, nargs='?', const=1, default=0.800)
    parser.add_argument("--albedo_of_surface", help="albedo of surface", type=float, nargs='?', const=1, default=0.4)
    args = parser.parse_args()

    return args


def output(current_tick, white_num, black_num, solar_luminosity, global_temperature):
    print("current_tick", current_tick, "white_num", white_num, "black_num", black_num, 
          "solar_luminosity", solar_luminosity, "global_temperature", global_temperature)

#
class Simulator(object):

    def __init__(self, args):
        self.total_ticks = args.ticks
        self.start_whites = args.start_whites
        self.start_blacks = args.start_blacks
        self.albedo_whites = args.albedo_whites
        self.albedo_blacks = args.albedo_blacks
        self.albedo_of_surface = args.albedo_of_surface
        self.scenario = args.scenario
        self.solar_luminosity = args.solar_luminosity
        self.DIFFUSE_PERCENT = 50
        self.black_num = 0
        self.white_num = 0
        self.global_temperature = 0
        self.current_tick = 0

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

    def get_patch_with_daisy(self):
        patch_with_daisy_list = []
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                if patch.get_daisy() != None:
                    patch_with_daisy_list.append(patch)
        return patch_with_daisy_list

    def check_survivability_handler(self):
        patch_with_daisy_list = self.get_patch_with_daisy()
        for patch in patch_with_daisy_list:
            if patch.check_survivability() is True:
                # print (rand_patch.get_daisy())
                neighbors_pos_list = []
                neighbors_pos = self.get_neighbors(patch.x, patch.y)
                # print (neighbors_pos)
                for j in range(0, len(neighbors_pos)):
                    if (neighbors_pos[j] != None):
                        neighbors_pos_list.append(neighbors_pos[j])
                # print (neighbors_pos_list)
                while True:
                    if len(neighbors_pos_list) == 0: break
                    rand_index = random.randint(0, len(neighbors_pos_list)-1)
                    neighbor_pos = neighbors_pos_list[rand_index]
                    del neighbors_pos_list[rand_index]
                    neighbor = patch_graph[neighbor_pos]
                    if neighbor.get_daisy() is None:
                        # print("Set daisy at", neighbor.x, neighbor.y)
                        if patch.get_daisy().get_color() == Color.WHITE:
                            albedo = self.albedo_whites
                        if patch.get_daisy().get_color() == Color.BLACK:
                            albedo = self.albedo_blacks
                        neighbor.set_daisy(patch.get_daisy().get_color(), albedo)
                        break
        # num = len(patch_list)
        # for i in range(0, num):
        #     rand_patch, patch_list = self.get_random_patch(patch_list)
        #     if rand_patch is None:
        #         return
            # seed a same type daisy if true
            # if rand_patch.check_survivability() is True:
            #     # print (rand_patch.get_daisy())
            #     neighbors_pos_list = []
            #     neighbors_pos = self.get_neighbors(rand_patch.x, rand_patch.y)
            #     # print (neighbors_pos)
            #     for j in range(0, len(neighbors_pos)):
            #         if (neighbors_pos[j] != None):
            #             neighbors_pos_list.append(neighbors_pos[j])
            #     # print (neighbors_pos_list)
            #     while True:
            #         if len(neighbors_pos_list) == 0: break
            #         rand_index = random.randint(0, len(neighbors_pos_list)-1)
            #         neighbor_pos = neighbors_pos_list[rand_index]
            #         del neighbors_pos_list[rand_index]
            #         neighbor = patch_graph[neighbor_pos]
            #         if neighbor.get_daisy() is None:
            #             # print("Set daisy at", neighbor.x, neighbor.y)
            #             neighbor.set_daisy(rand_patch.get_daisy().get_color())
            #             break
    
    '''
    deal with diffuse. to finish the function of diffuse in NetLogo
    equal: diffuse temperature .5
    '''
    def diffuse_handler(self):
        # New version
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                diffuse_temperature = patch.get_temperature() * self.DIFFUSE_PERCENT / 100
                # print(diffuse_temperature)
                patch.set_temperature(patch.get_temperature() - diffuse_temperature)
                neighbors = []
                neighbors_pos = self.get_neighbors(patch.x, patch.y)
                for neighbor_pos in neighbors_pos:
                    if neighbor_pos != None:
                        neighbors.append(patch_graph[neighbor_pos])
                for neighbor in neighbors:
                    neighbor.set_temperature(neighbor.get_temperature() + diffuse_temperature / len(neighbors))
    
        # calculate how much the patch lose and receive
        # for x in range(MIN_XCOR, MAX_XCOR):
        #     for y in range(MIN_YCOR, MAX_YCOR):
        #         pos = str(x) + "," + str(y)
        #         patch = patch_graph[pos]
        #         diffuse_unit = patch.get_temperature() * self.DIFFUSE_PERCENT / 100 / 8
        #         patch.set_temperature( patch.get_temperature() * (100 - self.DIFFUSE_PERCENT) / 100)
        #         for neighbour_pos in self.get_neighbors(x,y):
        #             if (neighbour_pos == None):
        #                 continue
        #             diffused_patch = patch_graph[neighbour_pos]
        #             diffused_patch.set_receiced_diffuse(diffused_patch.get_receiced_diffuse() + diffuse_unit)
        
        # # # update the lose and received temperature.
        # for x in range(MIN_XCOR, MAX_XCOR):
        #     for y in range(MIN_YCOR, MAX_YCOR):
        #         pos = str(x) + "," + str(y)
        #         patch = patch_graph[pos]
        #         patch.set_temperature(patch.get_temperature() + patch.get_receiced_diffuse())
        #         patch.set_receiced_diffuse(0)

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
        total_patch = (MAX_XCOR - MIN_XCOR) * (MAX_YCOR - MIN_YCOR)
        white_daisies_num = round(total_patch * self.start_whites / 100)
        black_daisies_num = round(total_patch * self.start_blacks / 100)
        for white_count in range(0, white_daisies_num):
            empty_patch, empty_patch_list = self.get_random_patch(empty_patch_list)
            if empty_patch != None:
                empty_patch.set_daisy(Color.WHITE, self.albedo_whites)
                patch_graph[empty_patch.x, empty_patch.y] = empty_patch
        for black_count in range(0, white_daisies_num):
            empty_patch, empty_patch_list = self.get_random_patch(empty_patch_list)
            if empty_patch != None:
                empty_patch.set_daisy(Color.BLACK, self.albedo_blacks)
                patch_graph[empty_patch.x, empty_patch.y] = empty_patch

    def calc_temperature(self):
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                patch.calculate_local_temperature(self.albedo_of_surface, self.solar_luminosity)

    def get_daisy_num(self, color):
        num = 0
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                if patch.get_daisy() != None:
                    if(patch.get_daisy().get_color() == color):
                        num += 1
        return num

    def cal_global_temperature(self):
        total_temperature = 0
        for x in range(MIN_XCOR, MAX_XCOR):
            for y in range(MIN_YCOR, MAX_YCOR):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                total_temperature += patch.get_temperature()
        total_patch = (MAX_XCOR - MIN_XCOR) * (MAX_YCOR - MIN_YCOR)
        self.global_temperature = total_temperature / total_patch
        

    def initialize(self):

        if (self.scenario == "low-solar-luminosity"):
                self.solar_luminosity = 0.6
            
        if (self.scenario == "our-solar-luminosity"):
            self.solar_luminosity = 1
        
        if (self.scenario == "high-solar-luminosity"):
            self.solar_luminosity = 1.4
        
        if (self.scenario == "ramp-up-ramp-down"):
            if (self.current_tick > 200 and self.current_tick <= 400):
                # 保留4位小数
                self.solar_luminosity = float(format((self.solar_luminosity + 0.005), '.4f'))
            if (self.current_tick > 600 and self.current_tick <= 850):
                self.solar_luminosity = float(format((self.solar_luminosity - 0.0025), '.4f'))
        
        self.set_up_patch_graph()
        self.seed_daisies_randomly()
        # ask patches [calc-temperature]
        self.calc_temperature()
        self.cal_global_temperature()

        
        
    def update_every_tick(self):
        while(self.current_tick <= self.total_ticks):
            self.white_num = self.get_daisy_num(Color.WHITE)
            self.black_num = self.get_daisy_num(Color.BLACK)
            output(self.current_tick, self.white_num, self.black_num, self.solar_luminosity, self.global_temperature)
            
            # equal: ask patches [calc-temperature]
            self.calc_temperature()

            # equal: diffuse temperature .5
            self.diffuse_handler()

            # equal: ask daisies [check-survivability]
            self.check_survivability_handler()

            # equal: set global-temperature (mean [temperature] of patches)
            self.cal_global_temperature()

            self.current_tick += 1
            
            if (self.scenario == "low-solar-luminosity"):
                self.solar_luminosity = 0.6
            
            if (self.scenario == "our-solar-luminosity"):
                self.solar_luminosity = 1
            
            if (self.scenario == "high-solar-luminosity"):
                self.solar_luminosity = 1.4
            
            if (self.scenario == "ramp-up-ramp-down"):
                if (self.current_tick > 200 and self.current_tick <= 400):
                    # 保留4位小数
                    self.solar_luminosity = float(format((self.solar_luminosity + 0.005), '.4f'))
                if (self.current_tick > 600 and self.current_tick <= 850):
                    self.solar_luminosity = float(format((self.solar_luminosity - 0.0025), '.4f'))

    def test(self):
        self.initialize()
        self.update_every_tick()
        # self.set_up_patch_graph()
        # self.check_survivability_handler()
        # self.diffuseHandler()
        # white_count = 0
        # black_count = 0
        # for x in range(MIN_XCOR, MAX_XCOR):
        #     for y in range(MIN_YCOR, MAX_YCOR):
        #         pos = str(x) + "," + str(y)
        #         patch = patch_graph[pos]
        #         if patch.get_daisy() != None:
        #             if(patch.get_daisy().get_color() == Color.WHITE):
        #                 white_count += 1
        #             if(patch.get_daisy().get_color() == Color.BLACK):
        #                 black_count += 1
        # print("white_count", white_count)
        # print("black_count", black_count)

if __name__ == "__main__":
    daisy_world = Simulator(get_input())
    daisy_world.test()
