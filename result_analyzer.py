# @Time        :  2021-05-27
# @Author      :  Yuyao Ma       1111182,
#                 Chenqi Ni	    980329,
#                 Zhaochen Fan   1077663
# @Description :  This file is a helper tool to draw pictures for results
#                 generated by the project

'''
This file is used to generate 'Luminosity-tick' figure, 
, 'Global_temperature-tick' figure and 'Population_temperature-tick' figure.
NOTE: This file may include some third-party library to generature the figures. 
It is an additional implementation and will not be included in the original 
assignment specification. 
'''

from abc import abstractproperty
import matplotlib.pyplot as plt
import argparse
import os

# Get result filename from command line
def get_input():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result_name", help="The name of result file",
                        nargs='?', const=1)
    args = parser.parse_args()
    return args

# Read the result file and create the result_list we want
def read_file(filepath):
    result_list = []
    index = 0
    with open(filepath, 'r') as f:
        for line in f:
            index += 1
            if index < 7:
                continue  
            if line[0] == 'P':
                continue
            string = ""
            one_group_list = []
            time = 0
            for i in line:
                if i == (' ') or i ==('\t'):
                    time += 1
                    if time == 1:
                        one_group_list.append(string)
                    else:
                        string = ""
                else:
                    time = 0
                    string += i
            result_list.append(one_group_list)
    return result_list

# Draw tick_luminosity figure
def draw_tick_luminosity(tick_list, luminosity_list, dir_name):
    # plt.figure(figsize=(10, 10))
    plt.plot(tick_list, luminosity_list, linewidth = 3)
    plt.title("Luminosity", fontsize = 20)
    plt.xlabel("tick", fontsize = 15)
    plt.ylabel("luminosity", fontsize = 15)
    plt.tick_params(axis='both', labelsize=15)
    plt.savefig(dir_name + '/luminosity.png')
    plt.show()

# Draw tick_global_temperature figure
def draw_tick_global_temperature(tick_list, global_temperature_list, dir_name):
    # plt.figure(figsize=(10, 10))
    plt.plot(tick_list, global_temperature_list, linewidth = 3)
    plt.title("Global Temperature", fontsize = 20)
    plt.xlabel("tick", fontsize = 15)
    plt.ylabel("temperature", fontsize = 15)
    plt.tick_params(axis='both', labelsize=15)
    plt.savefig(dir_name + '/temperature.png')
    plt.show()

# Draw tick_population figure
def draw_tick_population(tick_list, white_num_list, black_num_list, dir_name):
    # plt.figure(figsize=(10, 10))
    plt.plot(tick_list, white_num_list, color='blue', \
        label='white daisies population')
    plt.plot(tick_list, black_num_list, color='black', \
        label='black daisies population')
    plt.legend()
    plt.title("Population", fontsize = 20)
    plt.xlabel("tick", fontsize = 15)
    plt.ylabel("Number", fontsize = 15)
    plt.tick_params(axis='both', labelsize=15)
    plt.savefig(dir_name + '/population.png')
    plt.show()

# Main function for lauching the analyzer
def main():
    args = get_input()
    result_name = args.result_name
    if result_name is None:
        print("Please input the result file name.")
        return
    result_list = read_file(result_name)
    tick_list = []
    white_num_list = []
    black_num_list = []
    luminosity_list = []
    global_temperature_list = []
    for result in result_list:
        tick_list.append(int(result[0]))
        white_num_list.append(int(result[1]))
        black_num_list.append(int(result[2]))
        luminosity_list.append(float(result[3]))
        global_temperature_list.append(float(result[4]))
    dir_name = result_name[0:-4]
    isExists=os.path.exists(dir_name)
    if not isExists:
        os.makedirs(dir_name) 
    draw_tick_luminosity(tick_list, luminosity_list, dir_name)
    draw_tick_global_temperature(tick_list, global_temperature_list, dir_name)
    draw_tick_population(tick_list, white_num_list, black_num_list, dir_name)

if __name__ == "__main__":
    main()
