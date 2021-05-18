import argparse
import random
from daisy import Color
from patch import Patch

# NetLogo has 29 * 29 pathches
MIN_XCOR = 0
MAX_XCOR = 28
MIN_YCOR = 0
MAX_YCOR = 28

# Use patch_graph to store the maping between coordinate and patch
# Format: {(x,y): patch}
patch_graph = {}

# Get input from command line
def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticks", help="total ticks, Default: Infinite", type=float, nargs='?', const=1, default=float('inf'))
    parser.add_argument("--max_age", help="The max age of daisy", type=int, nargs='?', const=1, default=25,
                        choices=range(0, 1000))
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
    parser.add_argument("--pollution_level", help="The pollution_level is extension part, which simulates the human's pollution. \
        It has 3 levels: 1-Low; 2-Medium; 3-High. The default value is 0 namely no pollution", type=int, nargs='?', const=1, default=0)
    args = parser.parse_args()
    return args

# Format the output
def output(current_tick, white_num, black_num, solar_luminosity, global_temperature):
    print("current_tick", current_tick, "white_num", white_num, "black_num", black_num, 
          "solar_luminosity", solar_luminosity, "global_temperature", global_temperature)

class daisy_world(object):
    def __init__(self, args):
        self.total_ticks = args.ticks
        self.start_whites = args.start_whites
        self.start_blacks = args.start_blacks
        self.albedo_whites = args.albedo_whites
        self.albedo_blacks = args.albedo_blacks
        self.albedo_of_surface = args.albedo_of_surface
        self.scenario = args.scenario
        self.solar_luminosity = args.solar_luminosity
        self.max_age = args.max_age
        self.pollution_level = args.pollution_level
        self.DIFFUSE_PERCENT = 50
        self.black_num = 0
        self.white_num = 0
        self.global_temperature = 0
        self.current_tick = 0

    def initialize_patch_graph(self):
        # In python, range() is left-closed and right-open interval
        for x in range(MIN_XCOR, MAX_XCOR + 1):
            for y in range(MIN_YCOR, MAX_YCOR + 1):
                position = str(x) + "," + str(y)
                patch = Patch(x, y)
                patch_graph[position] = patch

    # Get a random patch from a patch_list
    def get_random_patch(self, patch_list):
        # If the patch_list is empty, return None
        if len(patch_list) == 0:
            return None
        random_index = random.randint(0, len(patch_list) - 1)
        random_patch = patch_list[random_index]
        # Delete the chosen patch in patch_list in order to avoid duplicate
        del patch_list[random_index]
        return random_patch, patch_list

    # Get the list of neighborhood patches of (x,y) coordinate
    def get_neighbors(self, patch):
        x = patch.x
        y = patch.y
        neighbors_list = []
        # up neighbor
        if y + 1 <= MAX_YCOR:
            position = str(x) + "," + str(y + 1)
            neighbors_list.append(patch_graph[position])
        # down neighbor
        if y - 1 >= MIN_YCOR:
            position = str(x) + "," + str(y - 1)
            neighbors_list.append(patch_graph[position])
        # left neighbor
        if x - 1 >= MIN_XCOR:
            position = str(x - 1) + "," + str(y)
            neighbors_list.append(patch_graph[position])
        # right neighbor
        if x + 1 <= MAX_XCOR:
            position = str(x + 1) + "," + str(y)
            neighbors_list.append(patch_graph[position])
        # left up neighbor
        if x - 1 >= MIN_XCOR and y + 1 <= MAX_YCOR:
            position = str(x - 1) + "," + str(y + 1)
            neighbors_list.append(patch_graph[position])
        # left down neighbor
        if x - 1 >= MIN_XCOR and y - 1 >= MIN_YCOR:
            position = str(x - 1) + "," + str(y - 1)
            neighbors_list.append(patch_graph[position])
        # right up neighbor
        if x + 1 <= MAX_XCOR and y + 1 <= MAX_YCOR:
            position = str(x + 1) + "," + str(y + 1)
            neighbors_list.append(patch_graph[position])
        # right down neighbor
        if x + 1 <= MAX_XCOR and y - 1 >= MIN_YCOR:
            position = str(x + 1) + "," + str(y - 1)
            neighbors_list.append(patch_graph[position])
        return neighbors_list

    # Get the list of patch where has daisy
    def get_patch_with_daisy(self):
        patch_with_daisy_list = []
        for x in range(MIN_XCOR, MAX_XCOR + 1):
            for y in range(MIN_YCOR, MAX_YCOR + 1):
                position = str(x) + "," + str(y)
                patch = patch_graph[position]
                if patch.get_daisy() != None:
                    patch_with_daisy_list.append(patch)
        return patch_with_daisy_list

    # 'to check-survivability' procedure in NetLogo code
    def check_survivability(self):
        patch_with_daisy_list = self.get_patch_with_daisy()
        for patch in patch_with_daisy_list:
            if patch.check_survivability() is True:
                neighbors_list = self.get_neighbors(patch)
                while True:
                    if len(neighbors_list) == 0: 
                        break
                    # Choose a random neighbor to seed in case of common 
                    # neighbor for patch with WHITE daisy and patch with 
                    # BLACK daisy happened
                    random_index = random.randint(0, len(neighbors_list)-1)
                    neighbor = neighbors_list[random_index]
                    del neighbors_list[random_index]
                    if neighbor.get_daisy() is None:
                        if patch.get_daisy().get_color() == Color.WHITE:
                            albedo = self.albedo_whites
                        if patch.get_daisy().get_color() == Color.BLACK:
                            albedo = self.albedo_blacks
                        neighbor.set_daisy(patch.get_daisy().get_color(), albedo, self.max_age)

    # 'diffuse temperature .5' procedure in NetLogo code
    def diffuse(self):
        for x in range(MIN_XCOR, MAX_XCOR + 1):
            for y in range(MIN_YCOR, MAX_YCOR + 1):
                position = str(x) + "," + str(y)
                patch = patch_graph[position]
                diffuse_temperature = patch.get_temperature() * self.DIFFUSE_PERCENT / 100
                patch.set_temperature(patch.get_temperature() - diffuse_temperature)
                neighbors_list = self.get_neighbors(patch)
                for neighbor in neighbors_list:
                    neighbor.set_temperature(neighbor.get_temperature() + diffuse_temperature / len(neighbors_list))
    
    def get_empty_patch_list(self):
        empty_patch_list = []
        for x in range(MIN_XCOR, MAX_XCOR + 1):
            for y in range(MIN_YCOR, MAX_YCOR + 1):
                position = str(x) + "," + str(y)
                patch = patch_graph[position]
                if patch.get_daisy() is None:
                    empty_patch_list.append(patch)
        return empty_patch_list

    # 'seed-whites-randomly' and 'seed-blacks-randomly' procedures in NetLogo
    def seed_daisies_randomly(self):
        empty_patch_list = self.get_empty_patch_list()
        total_patch = (MAX_XCOR - MIN_XCOR + 1) * (MAX_YCOR - MIN_YCOR + 1)
        white_daisies_num = round(total_patch * self.start_whites / 100)
        black_daisies_num = round(total_patch * self.start_blacks / 100)
        for white_count in range(0, white_daisies_num):
            empty_patch, empty_patch_list = self.get_random_patch(empty_patch_list)
            if empty_patch != None:
                empty_patch.set_daisy(Color.WHITE, self.albedo_whites, self.max_age)
                patch_graph[empty_patch.x, empty_patch.y] = empty_patch
        for black_count in range(0, white_daisies_num):
            empty_patch, empty_patch_list = self.get_random_patch(empty_patch_list)
            if empty_patch != None:
                empty_patch.set_daisy(Color.BLACK, self.albedo_blacks, self.max_age)
                patch_graph[empty_patch.x, empty_patch.y] = empty_patch

    # 'calc-temperature' procedure in NetLogo
    def calc_temperature(self):
        for x in range(MIN_XCOR, MAX_XCOR + 1):
            for y in range(MIN_YCOR, MAX_YCOR + 1):
                position = str(x) + "," + str(y)
                patch = patch_graph[position]
                patch.calculate_local_temperature(self.albedo_of_surface, self.solar_luminosity)

    # Get the number of WHITE or BLACK daisy
    def get_daisy_num(self, color):
        num = 0
        for x in range(MIN_XCOR, MAX_XCOR + 1):
            for y in range(MIN_YCOR, MAX_YCOR + 1):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                if patch.get_daisy() != None:
                    if(patch.get_daisy().get_color() == color):
                        num += 1
        return num

    # 'set global-temperature (mean [temperature] of patches)' in NetLogo
    def cal_global_temperature(self):
        total_temperature = 0
        for x in range(MIN_XCOR, MAX_XCOR + 1):
            for y in range(MIN_YCOR, MAX_YCOR + 1):
                pos = str(x) + "," + str(y)
                patch = patch_graph[pos]
                total_temperature += patch.get_temperature()
        total_patch = (MAX_XCOR - MIN_XCOR + 1) * (MAX_YCOR - MIN_YCOR + 1)
        self.global_temperature = total_temperature / total_patch
    
    # 'to setup' in NetLogo
    def setup(self):
        if (self.scenario == "low-solar-luminosity"):
                self.solar_luminosity = 0.6

        if (self.scenario == "our-solar-luminosity"):
            self.solar_luminosity = 1
        
        if (self.scenario == "high-solar-luminosity"):
            self.solar_luminosity = 1.4
        
        if (self.scenario == "ramp-up-ramp-down"):
            if (self.current_tick > 200 and self.current_tick <= 400):
                # Keep 4 decimal places
                self.solar_luminosity = float(format((self.solar_luminosity + 0.005), '.4f'))
            if (self.current_tick > 600 and self.current_tick <= 850):
                self.solar_luminosity = float(format((self.solar_luminosity - 0.0025), '.4f'))
        
        self.initialize_patch_graph()

        # 'seed-blacks-randomly' and 'seed-whites-randomly' in NetLogo
        self.seed_daisies_randomly()

        # 'ask patches [calc-temperature]' in NetLogo
        self.calc_temperature()

        # 'set global-temperature (mean [temperature] of patches)' in NetLogo
        self.cal_global_temperature()

    # Extension: humam pollution
    # 1 - Low: Destroy 10% alive daisies randomly every 50 ticks
    # 2 - Medium: Destroy 25% alive daisies randomly every 50 ticks
    # 3 - High: Destroy 50% alive daisies randomly every 50 ticks
    def pollution_simulation(self, pollution_level):
        destroyed_percentage = 0
        if (pollution_level == 1):
            destroyed_percentage = 0.1
        if (pollution_level == 2):
            destroyed_percentage = 0.25
        if (pollution_level == 3):
            destroyed_percentage = 0.5
        
        white_num = self.get_daisy_num(Color.WHITE)
        black_num = self.get_daisy_num(Color.BLACK)
        total_num = white_num + black_num
        destroyed_num = total_num * destroyed_percentage
        
        patch_with_daisy_list = self.get_patch_with_daisy()

        for num in range(0, int(destroyed_num)):
            if len(patch_with_daisy_list) == 0:
                break
            random_patch, patch_with_daisy_list = self.get_random_patch(patch_with_daisy_list)
            postion = str(random_patch.x) + ',' + str(random_patch.y) 
            patch_graph[postion].set_daisy_as_None()

        print("Pollution Happened. Level:", pollution_level)

    # 'to go' in NetLogo
    def update_every_tick(self):
        while(self.current_tick <= self.total_ticks):
            # Extention
            if self.pollution_level != 0:
                if self.current_tick % 50 == 0:
                    self.pollution_simulation(self.pollution_level)

            self.white_num = self.get_daisy_num(Color.WHITE)
            self.black_num = self.get_daisy_num(Color.BLACK)
            output(self.current_tick, self.white_num, self.black_num, self.solar_luminosity, self.global_temperature)
            
            # '0ask patches [calc-temperature]' in NetLogo
            self.calc_temperature()

            # 'diffuse temperature .5' in NetLogo
            self.diffuse()

            # 'ask daisies [check-survivability]' in NetLogo
            self.check_survivability()

            # 'set global-temperature (mean [temperature] of patches)' in NetLogo
            self.cal_global_temperature()

            # 'tick' in NetLogo
            self.current_tick += 1
            
            if (self.scenario == "low-solar-luminosity"):
                self.solar_luminosity = 0.6
            
            if (self.scenario == "our-solar-luminosity"):
                self.solar_luminosity = 1
            
            if (self.scenario == "high-solar-luminosity"):
                self.solar_luminosity = 1.4
            
            if (self.scenario == "ramp-up-ramp-down"):
                if (self.current_tick > 200 and self.current_tick <= 400):
                    # Keep 4 decimal places
                    self.solar_luminosity = float(format((self.solar_luminosity + 0.005), '.4f'))
                if (self.current_tick > 600 and self.current_tick <= 850):
                    self.solar_luminosity = float(format((self.solar_luminosity - 0.0025), '.4f'))

    def start_simulation(self):
        self.setup()
        self.update_every_tick()