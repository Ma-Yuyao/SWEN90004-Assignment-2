# University of Melbourne Modelling Complex Software Systems (SWEN90004) - Assignment 2

- Course: [Modelling Complex Software Systems](https://handbook.unimelb.edu.au/2021/subjects/swen90004)
- Instructor: [Dr. Artem Polyvyanyy](http://polyvyanyy.com/)

| Student Name  | Student ID |
| ------------- | ------------- |
| Chenqi Ni   | 980329 |
| Zhaochen Fan   | 1077663 |
| Yuyao Ma | 1111182 |

## How to use

*[simulator.py]*(simulator.py) is the entry point of the program. It accepts the following parameters. The default values will be assigned to unspecified parameters.

'''python
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
'''
<!-- 
Launch command example:
    /* Program will run 1000 ticks under the default configuration. */
    java Simulator -ticks 1000

    /* -start-%-whites=25, -albedo-of-whites=0.8 -start-%-blacks=25 -albedo-of-blacks=0.20 
     * Program will run 1000 ticks.
     */
    java Simulator -ticks 1000 -start-%-whites 25 -albedo-of-whites 0.8 -start-%-blacks 25 -albedo-of-blacks 0.20
    
    /*
     * scenario is ramp-up-ramp-down. Program will run 1000 ticks.
     * note: according to the scenario you specify, -solar-luminosity will be covered even if you alreadly specify its value
     */
     java Simulator -ticks 1000 -scenario ramp-up-ramp-down

     /*
      * generate 50 male rabbits and 80 female rabbits. Program will run 1000 ticks.
      */
    java Simulator -ticks 1000 -start-male-rabbits 50 -start-female-rabbits 80

After launch the program, it will print the configuration firstly. If the input parameters are wrong, it will give you corresponding wrong information. If the input parameters are right, it should generate a csv file called "output.csv".
```python
python3 simulator.py
``` -->