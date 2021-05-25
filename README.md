# Modelling Complex Software Systems (SWEN90004) - Assignment 2

- Course: [University of Melbourne - Modelling Complex Software Systems](https://handbook.unimelb.edu.au/2021/subjects/swen90004)
- Instructor: [Dr. Artem Polyvyanyy](http://polyvyanyy.com/)

| Student Name  | Student ID |
| ------------- | ------------- |
| Chenqi Ni   | 980329 |
| Zhaochen Fan   | 1077663 |
| Yuyao Ma | 1111182 |

## How to use

[simulator.py](simulator.py) is the entry point of the program. It accepts the following parameters. The default values will be assigned to unspecified parameters.

```python
--x  # Num of X-coordinate of daisy world (start from 0), Default: 28
--y  # Num of Y-coordinate of daisy world (start from 0), Default: 28
--ticks  # Total ticks, Default: Infinite
--max_age  # The max age of daisy, Default: 25
--start_white  # The percent of white daisies when setup, Default: 20
--start_blacks # The percent of black daisies when setup, Default: 20
--albedo_whites  # The albedo of white daisies, Default: 0.75
--albedo_blacks  # The albedo of black daisies, Default: 0.25
--scenario  # The scenario you would like to set, five possible scenarios: "ramp-up-ramp-down", "low-solar-luminosity", "our-solar-luminosity", "high-solar-luminosity", "maintain-current-luminosity", Default: "our-solar-luminosity"
--solar_luminosity  # The solar luminosity you would like to set. NOTE: This only works if the scenario is maintain-current-luminosity
--albedo_of_surface  # The albedo of surface, Default: 0.4
--pollution_level  # The pollution_level is extension part, which simulates the human's pollution. It has 3 levels: 1-Low; 2-Medium; 3-High. The default value is 0 namely no pollution, Default: 0
--pollution_frequency  # How many ticks does one pollution occur, Default: 25
```

Examples:

```python
python3 simulator.py # Run the program with all arguments of default values
```

```python
python3 simulator.py --x 20 --y 20 --ticks 1000 --max_age 100 --scenario high-solar-luminosity 
# Run the program with 21 * 21 maps, 1000 ticks, 100 as max age of the daisy, and high-solar-luminosity scenario, and other arguments of default values
```

```python
python3 simulator.py --pollution_level 3 --pollution_frequency 10
# Run the program with 3 pollution level as well as every 10 ticks pollution frequency, and other arguments of default values
```


After running the program, it will print the key information as well the update for each tick on command lind. Besides, a result file containing key information named "result_$local_time.out" (i.e. "result_2021-05-25_23-30-12.out") will be generated.

## Additional Tool for analysis

We also achieve an analysis tool [result_analyzer.py](simulator.py) for generating 'Luminosity-tick' figure, 'Global_temperature-tick' figure and 'Population_temperature-tick' figure.

**NOTE**: This file may include some third-party library to generature the figures. It is an additional implementation and will not be included in the original assignment specification. 

### How to use
Let's say the filename of result file is "result_2021-05-25_23-30-12.out". Use the below command to start the analyzer.

```python
python3 result_analyzer.py --result_name result_2021-05-25_23-30-12.out
```

If it says "Some model is not found", please install the required model manually.

Then three figures will be generated and displayed individually. And a folder named "result_2021-05-25_23-46-13" containing these three figures will also be generated.

Thanks a lot for the guidance of the teaching team!
