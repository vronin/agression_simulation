import random
import math
import time
import string

# World setup
INITIAL_POPULATION_SIZE = 500
INITIAL_MALEVALENCE_MEAN = 0.5
INITIAL_MALEVALENCE_DEVIATION = 0.1
WORLD_DIMENSION_X = 100
WORLD_DIMENSION_Y = 100


# Number of steps to simular
SIMULATION_STEPS = 150

# Demographics related things
# I have no idea why, but to ballance real actuary table I had to bump up birth rate pretty high
BIRTH_RATE = 2.5 / 100
MAX_AGE = 120
# Real actuary table (I believe for US, males)
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

# Coming of Age
AGE_OF_COMING_OF_AGE = 15
BEHAVIOUR_INFLUENCERS_DISTANCE = 5 

# Cop related info
COP_CRIME_DETECTION_DISTANCE = 10
COP_RETIREMENT_AGE = 50
COP_PROMOTION_AGE = 21
COP_PROMOTION_PROBABILITY = 0.01
COP_DEFENCE_PROBABILITY = 0.7

# Attack related info
ATTACK_DEATH_PROBABILITY = 0.1
# We use this factor to make it non-lineary relation between malevolence and whether they will attack
# The smaller number, the less likely they will attack (even if they are malevolent)
ATTACK_EXPONENT_FACTOR=0.15
DEFENCE_EXPONENT_FACTOR=0.7

# Miscellanious
COORDINATE_CHANGE = 5

# A record of committed crime
class RapRecord:
    def __init__(self, attacker_id, victim_id):
        self.attacker_id = attacker_id
        self.victim_if = victim_id

class Person:
    def __init__(self, age):
        self.id = ''.join(random.choices(string.ascii_lowercase, k=8))
        self.x = random.randint(0, WORLD_DIMENSION_X)
        self.y = random.randint(0, WORLD_DIMENSION_Y)
        self.age = age
        self.malevolence = 0.0 if self.age < AGE_OF_COMING_OF_AGE else random.gauss(INITIAL_MALEVALENCE_MEAN, INITIAL_MALEVALENCE_DEVIATION)
        self.cop = False

    def __str__(self):
        return f"Person: Lives at ({self.x}, {self.y}), age {self.age}, malevolence {self.malevolence}"

    def chance_of_death(self):
        return ACTUARY_TABLE[self.age]

    def is_near(self, other, distance):
        # Physical distance between people
        return abs(self.x - other.x) < distance and abs(self.y - other.y) < distance

def create_world():    
    # Initialize population with random coordinates
    population = []
    for i in range(INITIAL_POPULATION_SIZE):
        population.append(Person(random.randint(0, MAX_AGE)))
    return population
    
def births(population):    
    # Add newborn babies to the population. They magically are born at random places
    birth_count = int(len(population) * BIRTH_RATE)
    population += [Person(0) for _ in range(birth_count)]

    return birth_count

def deaths(population, memorial_list):
    surviving_population = []
    for person in population:
        if random.random() > person.chance_of_death():
            surviving_population += [person]
        else:
            memorial_list += [person]
    return surviving_population

def people_around_me(population, person, distance):
    return [other for other in population if person.is_near(other, distance) and person != other]

def coming_of_age(population):
    coming_of_age_count = 0
    for person in population:
        # Initialize malevolence factor for people who have just turned 15
        if person.age == AGE_OF_COMING_OF_AGE and person.malevolence == 0.0:
            # Calculate the average malevolence of people nearby. If there are nobody nearby, let's go with random
            people_around = people_around_me(population, person, BEHAVIOUR_INFLUENCERS_DISTANCE)
            adults_aroung = [other for other in people_around if other.age >= AGE_OF_COMING_OF_AGE]
            avg_malevolence = sum(other.malevolence for other in adults_aroung) / len(adults_aroung) if adults_aroung else INITIAL_MALEVALENCE_MEAN

            # Initialize malevolence using Gaussian distribution with a mean equal to the calculated average
            # Unfortunately, if people around you are malevolent, you will more likely to be malevolent too.
            person.malevolence = random.gauss(avg_malevolence, INITIAL_MALEVALENCE_DEVIATION)
            coming_of_age_count += 1
    return coming_of_age_count

def moving_around(population):
    for person in population:
        # People move around a bit
        person.x += random.randint(-COORDINATE_CHANGE, COORDINATE_CHANGE)
        person.y += random.randint(-COORDINATE_CHANGE, COORDINATE_CHANGE)

        # Wrap around coordinate grid
        person.x %= WORLD_DIMENSION_X
        person.y %= WORLD_DIMENSION_Y  
        
def aging(population):
     for person in population:
         person.age += 1

def attack(population, memorial_list, global_rap_sheet, attacker, victim, cop_reaction):    
    total_attacks = 0
    #print(f"Attacker {attacker.id} {attacker.cop}, {victim.id}, {victim.cop}, {cop_reaction}")

    if random.random() < ATTACK_DEATH_PROBABILITY:
        # Victim is deam
        if victim in population:
            memorial_list += [victim]
            population.remove(victim)
    else:
        # If victim is not dead, they may respond to attack (with higher chance than just randomly attacking somebody)
        if random.random() ** DEFENCE_EXPONENT_FACTOR < victim.malevolence:
            total_attacks += attack(population, memorial_list, global_rap_sheet, victim, attacker, False)

    # If this is cop reacting to a crime then other cops don't try to react to him
    if not cop_reaction:
        # If it's not a cop and there is a cop around, it reconds info about the attack and it may counter attack
        people_around = people_around_me(population, attacker, COP_CRIME_DETECTION_DISTANCE)
        for person in people_around:
            if person.cop:
                # Record for sure
                global_rap_sheet += [RapRecord(attacker.id, victim.id)]
                # Attack back probabilistically
                if random.random() < COP_DEFENCE_PROBABILITY:
                    total_attacks += attack(population, memorial_list, global_rap_sheet, person, attacker, True)
                # Only one cop react at a time right now
                break

    
    return total_attacks+1

def crime_time(population, memorial_list, global_rap_sheet):
    attacks_committed = 0
    for person in population:
        if random.random()**ATTACK_EXPONENT_FACTOR < person.malevolence:
            # Ready to commit a crime
            people_around = people_around_me(population, person, 5)
            if (len(people_around) == 0):
                continue
            victim = people_around[int(random.random()*len(people_around))]
            attacks_committed += attack(population, memorial_list, global_rap_sheet, person, victim, False)
            
    return attacks_committed

def cop_promotion_demotion(population):
    total_cops = 0
    for person in population:
        if person.cop and person.age > COP_RETIREMENT_AGE:
            # time to retire
            person.cop = False
        if not person.cop and person.age > COP_PROMOTION_AGE and person.age < COP_RETIREMENT_AGE and random.random() < COP_PROMOTION_PROBABILITY:
            # time to promote a cop
            person.cop = True
        if person.cop:
            total_cops += 1 
    return total_cops


def simulate_world(population, memorial_list, global_rap_sheet):
    # Run simulation for specified number of steps
    for step in range(SIMULATION_STEPS):
        st = time.time()

        # Birth
        births_count = births(population)

        # Death
        population_count = len(population)
        population = deaths(population, memorial_list)        
        deaths_count = population_count - len(population)

        # Coming of age
        coming_of_age_count = coming_of_age(population)

        # Crime Time
        attacks_committed = crime_time(population, memorial_list, global_rap_sheet)

        # Miscellenious 
        moving_around(population)
        aging(population)
        total_cops = cop_promotion_demotion(population)

        print(f"G-d's view: A {step} year passed... ")
        print(f"  Births: {births_count}")
        print(f"  Natural deaths: {deaths_count}")
        print(f"  Coming of Age: {coming_of_age_count}, Population: {len(population)}")
        print(f"  Attacks (including self-defence): {attacks_committed}")
        print(f"  Cops: {total_cops}")
        print(f"  Global rap sheet: {len(global_rap_sheet)}")
        print(f"  Memorial list: {len(memorial_list)}")
        
    return population

                
population = create_world()
memorial_list = []
global_rap_sheet = []
population = simulate_world(population, memorial_list, global_rap_sheet)
