import numpy as np
from evolution import get_fitness_for_population
import os


def write_stats(stats: dict, file: str):

    # writes the column
    if stats['generation'] == 0:
        with open(file, 'w') as f:
            for i in range(len(stats.keys())):
                if i == len(stats.keys())-1:
                    f.write(f'{list(stats.keys())[i]}\n')
                    break

                f.write(f'{list(stats.keys())[i]},')

    # write the statistics for that gen
    with open(file, 'a') as f:
        for i in range(len(stats.keys())):
            if i == len(stats.keys())-1:
                f.write(f'{stats[list(stats.keys())[i]]}\n')
                break

            f.write(f'{stats[list(stats.keys())[i]]},')


def gather_gen_stats(population: np.ndarray, gen: int, file: str):
    stats = {}

    stats['generation'] = gen
    stats['best'] = populations_best(population)
    stats['average'] = population_avg(population)
    stats['standard deviation'] = population_std(population)

    write_stats(stats, file)


def populations_best(population: np.ndarray):
    population_fitness = get_fitness_for_population(population)

    return np.max(population_fitness)


def population_avg(population: np.ndarray):
    population_fitness = get_fitness_for_population(population)

    return np.mean(population_fitness)


def population_std(population: np.ndarray):
    population_fitness = get_fitness_for_population(population)

    return np.std(population_fitness)
