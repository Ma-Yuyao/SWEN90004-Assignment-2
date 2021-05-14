import argparse

import numpy

# from pandas import np

solar_luminosity = 0.8
albedo_of_surface = 0.4


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
    parser.add_argument("--albedo_surface", help="albedo of surface", type=float, nargs='?', const=1, default=0.4,
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
        self.albedo_surface = args.albedo_surface
        self.scenario = args.scenario
        self.solar_luminosity = args.solar_luminosity

    def test(self):
        print(self.start_whites)
        print(self.albedo_surface)
        print(self.scenario)


    # def setup(self):

if __name__ == "__main__":

    daisy_world = Simulator(get_input())
    daisy_world.test()
