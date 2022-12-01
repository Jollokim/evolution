import numpy as np

from evolution import *

from logger import populations_best, gather_gen_stats

def run_evolution(arguments: dict):
    
    selection = arguments['selection']
    mutate = arguments['mutation']
    mutation_rate = arguments['mutation_rate']
    elites = arguments['elites']
    max_generation = arguments['max_generations']
    genom_size = arguments['genom_size']
    population_size = arguments['population_size']
    verbose = arguments['verbose']

    statistics_file = arguments['statistics_path']

    generation_count = 0
    population = create_initial_population(population_size, genom_size)
    

    # gather generation stats
    gather_gen_stats(population, generation_count, statistics_file)
    while not evolution_complete(population) and not generation_count == max_generation:
        
        # calculate fitness for all individuals
        population_fitness = get_fitness_for_population(population)

        if verbose:
            print()
            print('current gen')
            for ind in population:
                print(ind)

        # select parent of next generation
        population = selection(population, population_fitness, elites=elites)

        if verbose:
            print()
            print('gen after selection')
            for ind in population:
                print(ind)

        # mutate children from parents
        population = mutate(population, mutation_rate)

        if verbose:
            print()
            print('gen after mutation')
            for ind in population:
                print(ind)

        
        generation_count += 1

        if verbose:
            print('Generation:', generation_count, 'Best in gen:', populations_best(population))

        # gather generation stats
        gather_gen_stats(population, generation_count, statistics_file)

        






if __name__ == '__main__':
    import os

    arguments = {}

    # selection_rank or selection_cumulative
    arguments['selection'] = selection_fitness
    # constant_mutation or adaptive_mutation
    arguments['mutation'] = constant_mutation
    # for adaptive mutation rate is given as start mutation rate
    arguments['mutation_rate'] = 0.001
    # elites, can not be over half the population size
    arguments['elites'] = 2
    # max number of generation for each individual run
    arguments['max_generations'] = 10000
    # bit string size
    arguments['genom_size'] = 100
    # number of individuals for run
    arguments['population_size'] = 10
    # if True, prints the population for each step in one generation (current, after selection, after mutation)
    arguments['verbose'] = True

    # folder for statistics
    arguments['statistics_path'] = 'run1'

    os.makedirs(arguments['statistics_path'], exist_ok=True)

    # adding the stats file to path
    arguments['statistics_path'] += '/stats1.csv'
    
    run_evolution(arguments)