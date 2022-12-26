import random
import math

# Constants
INITIAL_POPULATION_SIZE = 10000
SIMULATION_STEPS = 150
COORDINATE_CHANGE = 5
# I have no idea why, but to ballance real actuary table I had to bump up birth rate pretty igh
BIRTH_RATE = 3.8 / 100
MAX_AGE = 120
WORLD_DIMENSION_X = 100
WORLD_DIMENSION_Y = 100
AGE_OF_COMING_OF_AGE = 15

ACTUARY_TABLE = [ 
    0.006081, 0.000425, 0.000260, 0.000194, 0.000154, 0.000142, 0.000135, 0.000127, 0.000116, 0.000104, 
    0.000097, 0.000106, 0.000144, 0.000220, 0.000323, 0.000437, 0.000552, 0.000675, 0.000806, 0.000939,
    0.001079, 0.001215, 0.001327, 0.001406, 0.001461, 0.001507, 0.001557, 0.001610, 0.001668, 0.001732,
    0.001795, 0.001858, 0.001923, 0.001992, 0.001992, 0.002145, 0.002231, 0.002316, 0.002398, 0.002482,
    0.002580, 0.002697, 0.002828, 0.002976, 0.003146, 0.003340, 0.003567, 0.003833, 0.004143, 0.004499,
    0.004890, 0.005321, 0.005810, 0.006363, 0.006973, 0.007629, 0.008322, 0.009049, 0.009806, 0.010595,
    0.011452, 0.012358, 0.013255, 0.014126, 0.015006, 0.016001, 0.017124, 0.018298, 0.019519, 0.020847,
    0.022381, 0.024185, 0.026266, 0.028660, 0.031401, 0.034618, 0.038263, 0.042190, 0.046367, 0.050948,
    0.056237, 0.062360, 0.069226, 0.076884, 0.085452, 0.095062, 0.105829, 0.105829, 0.131138, 0.145751,
    0.161678, 0.178905, 0.197408, 0.217149, 0.238080, 0.258821, 0.278966, 0.298092, 0.315762, 0.331550,
    0.348128, 0.365534, 0.383811, 0.403001, 0.423151, 0.444309, 0.466524, 0.489851, 0.514343, 0.540060,
    0.567063, 0.595417, 0.625187, 0.656447, 0.689269, 0.723732, 0.759919, 0.797915, 0.837811, 0.879701,    
    1
] 

class Person:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = random.randint(0, MAX_AGE)
        self.malevolence = 0.0 if self.age < AGE_OF_COMING_OF_AGE else random.random()

    def __str__(self):
        return f"Person: ({self.x}, {self.y}), age {self.age}, malevolence {self.malevolence}"

    def chance_of_death(self):
        return ACTUARY_TABLE[self.age]

    def is_near(self, other):
        # Physical distance between people
        return abs(self.x - other.x) < 5 and abs(self.y - other.y) < 5



def create_world():    
    # Initialize population with random coordinates
    population = []
    for i in range(INITIAL_POPULATION_SIZE):
        x = random.randint(0, WORLD_DIMENSION_X)
        y = random.randint(0, WORLD_DIMENSION_Y)
        population.append(Person(x, y))
    return population
    
def births(population):    
    # Add newborn babies to the population. They magically are born at random places
    population += [Person(random.randint(0, WORLD_DIMENSION_X), random.randint(0, WORLD_DIMENSION_Y)) for _ in range(int(len(population) * BIRTH_RATE))]

def deaths(population):
    return [person for person in population if random.random() > person.chance_of_death()]
    
def coming_of_age(population):
    for person in population:
        # Initialize malevolence factor for people who have just turned 15
        if person.age == AGE_OF_COMING_OF_AGE and person.malevolence == 0.0:
            # Calculate the average malevolence of people nearby. If there are nobody nearby, let's go with random
            near_people = [other for other in population if person.is_near(other) and other.age >= 15]
            avg_malevolence = sum(other.malevolence for other in near_people) / len(near_people) if near_people else random.random()

            # Initialize malevolence using Gaussian distribution with a mean equal to the calculated average
            # Unfortunately, if people around you are malevolent, you will more likely to be malevolent too.
            person.malevolence = random.gauss(avg_malevolence, 0.1)

def moving_around(population):
    for person in population:
        # People move around a bit
        person.x += random.randint(-COORDINATE_CHANGE, COORDINATE_CHANGE)
        person.y += random.randint(-COORDINATE_CHANGE, COORDINATE_CHANGE)

        # Wrap around coordinate grid
        person.x %= 100
        person.y %= 100  
        
def aging(population):
     for person in population:
         person.age += 1


def simulate_world(population):
    # Run simulation for specified number of steps
    for step in range(SIMULATION_STEPS):
        births(population)
        population = deaths(population)
        coming_of_age(population)
        moving_around(population)
        aging(population)
        print(f"--- A {step} year passed... Current population size {len(population)}")
        
    return population

                
population = create_world()
population = simulate_world(population)
