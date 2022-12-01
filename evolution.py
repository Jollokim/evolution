from individual import Individual
import numpy as np
import copy

import random


def adaptive_mutation(population: np.ndarray, mutation_rate=None):
    """
        Constant mutation rate over an individual
    """
    genom_size = len(population[0].genom)

    next_population = np.empty(len(population)*2, dtype=Individual)

    for i in range(len(population)):
        next_population[i] = copy.deepcopy(population[i])

    for i in range(len(population)):
        mutation_rate = (1 - (population[i].get_fitness() / len(population[i].genom)))

        for gene in range(genom_size):
            if random.random() < mutation_rate:
                if population[i].genom[gene] == 0:
                    population[i].genom[gene] = 1
                else:
                    population[i].genom[gene] = 0
        next_population[len(population)+i] = copy.deepcopy(population[i])

    return next_population

def constant_mutation(population: np.ndarray, mutation_rate: float):
    """
        Constant mutation rate over an individual
    """
    genom_size = len(population[0].genom)

    next_population = np.empty(len(population)*2, dtype=Individual)

    for i in range(len(population)):
        next_population[i] = copy.deepcopy(population[i])

    for i in range(len(population)):
        for gene in range(genom_size):
            if random.random() < mutation_rate:
                if population[i].genom[gene] == 0:
                    population[i].genom[gene] = 1
                else:
                    population[i].genom[gene] = 0
        next_population[len(population)+i] = copy.deepcopy(population[i])

    return next_population

def selection_fitness(population: np.ndarray, population_fitness: np.ndarray, elites: int = 0):
    rank_individual_dict = {}

    # rank the individuals based on fitness
    for i in range(len(population)):
        # find index for currently best individual
        argmax = np.argmax(population_fitness)

        # zero the fitness score to exclude it for next iteration
        population_fitness[argmax] = -1

        # set the individual with its given rank
        rank_individual_dict[i] = population[argmax]

    next_population = np.empty(len(population)//2, dtype=Individual)

    # add elites to next gen
    for i in range(elites):
        next_population[i] = rank_individual_dict[i]
        del rank_individual_dict[i]

    # create rank chance scheme
    rank_chances = []
    s = 0
    for i in range(elites, len(population)):
        s += rank_individual_dict[i].get_fitness()
        rank_chances.append(s)

    # create the remaining population
    survivor_population = np.empty(len(population)-elites, dtype=Individual)

    # add remaining individual to array
    for i in range(elites, len(population)):
        survivor_population[i-elites] = rank_individual_dict[i]

    # pick based on the rank_chances which of the remainor will be in the next generation
    for n in range(elites, len(population)//2):
        # pick a random number between lowest and highest value in rank_chances
        rand_num = np.random.randint(0, rank_chances[-1])

        # find which individual is going to be picked
        for i in range(len(rank_chances)):
            if i == (len(rank_chances)-1):
                next_population[n] = copy.deepcopy(survivor_population[0])
                break

            elif rank_chances[i] <= rand_num and rand_num < rank_chances[i+1]:
                next_population[n] = copy.deepcopy(survivor_population[i+1])
                break

    return next_population




def selection_rank(population: np.ndarray, population_fitness: np.ndarray, elites: int = 0):
    """
        Creates next generation by rank scheme with n-th triangular number.

        https://math.stackexchange.com/questions/60578/what-is-the-term-for-a-factorial-type-operation-but-with-summation-instead-of-p

        -1 (last rank individual) [0, 1>
        -2 [1, 3>
        -3 [3, 6>
        -4 [6, 10>
        etc. 
    """

    rank_individual_dict = {}

    # rank the individuals based on fitness
    for i in range(len(population)):
        # find index for currently best individual
        argmax = np.argmax(population_fitness)

        # zero the fitness score to exclude it for next iteration
        population_fitness[argmax] = -1

        # set the individual with its given rank
        rank_individual_dict[i] = population[argmax]

    next_population = np.empty(len(population)//2, dtype=Individual)

    # add elites to next gen
    for i in range(elites):
        next_population[i] = rank_individual_dict[i]
        del rank_individual_dict[i]

    # create rank chance scheme
    rank_chances = []
    s = 0
    for i in range(1, len(population)-elites+1):
        s += i
        rank_chances.append(s)

    # reverse comulation for convinience
    rank_chances.reverse()

    # create the remaining population
    survivor_population = np.empty(len(population)-elites, dtype=Individual)

    # add remaining individual to array
    for i in range(elites, len(population)):
        survivor_population[i-elites] = rank_individual_dict[i]

    # pick based on the rank_chances which of the remainor will be in the next generation
    for n in range(elites, len(population)//2):
        # pick a random number between lowest and highest value in rank_chances
        rand_num = np.random.randint(0, rank_chances[0])

        # find which individual is going to be picked
        for i in range(len(rank_chances)):
            if i == (len(rank_chances)-1):
                next_population[n] = copy.deepcopy(survivor_population[i])
                break

            if rank_chances[i] > rand_num and rand_num >= rank_chances[i+1]:
                next_population[n] = copy.deepcopy(survivor_population[i])
                break

    return next_population


def create_initial_population(population_size: int, geno_size: int):
    population = []

    for _ in range(population_size):
        genom = np.random.randint(0, 2, size=geno_size)

        individual = Individual(genom)

        population.append(individual)

    population = np.array(population, dtype=Individual)

    return population


def get_fitness_for_population(population: np.ndarray):
    population_fitness = np.zeros((len(population)))

    for i in range(len(population)):
        population_fitness[i] = population[i].get_fitness()

    return population_fitness


def evolution_complete(population: np.ndarray):
    for individual in population:
        if individual.is_perfect_individual():
            return True
    return False
