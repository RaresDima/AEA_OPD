import time
import statistics
import random
import multiprocessing
import pickle
import datetime

from deap import base
from deap import creator
from deap import tools

import opd_operators

import numpy as np
from matplotlib import pyplot as plt

np.set_printoptions(linewidth = 1000)


CONFIGURATIONS = {
                    'toy_old':
                    [
                        [10, 37, 14, 10, 0, 0],
                        [10, 37, 14, 9, 0, 0],
                        [10, 37, 14, 8, 0, 0],
                        [10, 37, 14, 7, 0, 0],
                        [10, 37, 14, 6, 0, 0],
                        [10, 37, 14, 5, 0, 0],
                    ],

                    'small_old':
                    [
                        [6, 50, 25, 15, 0, 0],
                        [6, 50, 25, 14, 0, 0],
                        [6, 50, 25, 13, 0, 0],
                        [6, 50, 25, 12, 0, 0],
                        [6, 50, 25, 11, 0, 0],
                        [6, 50, 25, 10, 0, 0],
                    ],

                    'medium_old':
                    [
                        [10, 100, 30, 15, 0, 0],
                        [10, 100, 30, 14, 0, 0],
                        [10, 100, 30, 13, 0, 0],
                        [10, 100, 30, 12, 0, 0],
                        [10, 100, 30, 11, 0, 0],
                        [10, 100, 30, 10, 0, 0],
                        [10, 100, 30, 9, 0, 0],
                        [10, 100, 30, 8, 0, 0],
                    ],

                    'real_old':
                    [
                        [15, 350, 100, 45, 0, 0],
                        [15, 350, 100, 40, 0, 0],
                        [15, 350, 100, 35, 0, 0],
                        [15, 350, 100, 34, 0, 0],
                        [15, 350, 100, 33, 0, 0],
                        [15, 350, 100, 32, 0, 0],
                        [15, 350, 100, 31, 0, 0],
                        [15, 350, 100, 30, 0, 0],
                    ],



                    'toy_improved':
                    [
                        [10, 37, 14, 10, 1, 5],
                        [10, 37, 14, 9, 1, 5],
                        [10, 37, 14, 8, 1, 5],
                        [10, 37, 14, 7, 1, 5],
                        [10, 37, 14, 6, 1, 5],
                        [10, 37, 14, 5, 1, 5],
                    ],

                    'small_improved':
                    [
                        [6, 50, 25, 15, 1, 5],
                        [6, 50, 25, 14, 1, 5],
                        [6, 50, 25, 13, 1, 5],
                        [6, 50, 25, 12, 1, 5],
                        [6, 50, 25, 11, 1, 5],
                        [6, 50, 25, 10, 1, 5],
                    ],

                    'medium_improved':
                    [
                        [10, 100, 30, 15, 1, 5],
                        [10, 100, 30, 14, 1, 5],
                        [10, 100, 30, 13, 1, 5],
                        [10, 100, 30, 12, 1, 5],
                        [10, 100, 30, 11, 1, 5],
                        [10, 100, 30, 10, 1, 5],
                        [10, 100, 30, 9, 1, 5],
                        [10, 100, 30, 8, 1, 5],
                    ],

                    'real_improved':
                    [
                        [15, 350, 100, 45, 1, 5],
                        [15, 350, 100, 40, 1, 5],
                        [15, 350, 100, 35, 1, 5],
                        [15, 350, 100, 34, 1, 5],
                        [15, 350, 100, 33, 1, 5],
                        [15, 350, 100, 32, 1, 5],
                        [15, 350, 100, 31, 1, 5],
                        [15, 350, 100, 30, 1, 5],
                    ]}

V, B, R = 10, 37, 14
TARGET_LAMBDA = 6

POPSIZE = 300
GENS = 500

CXPB = 0.5
MUTPB = 0.2

CX_K = 5

MUT_K = 5
MUT_GENEPB = 0.25

RUNS_PER_CONFIGURATION = 100


def run_opd_ga(toolbox: base.Toolbox,
               popsize: int,
               gens: int,
               cxpb: float,
               mutpb: float,
               elitism_k: int,
               new_inds_per_gen: int,
               target_lambda: int,
               verbose: bool = False):

    if verbose:
        print('Starting GA...')

    fitness_history = []

    pop = toolbox.generate_population(n = popsize)

    fitnesses = toolbox.parallel_map(toolbox.evaluate, pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    if verbose:
        print('Initial evaluation done.')

    fits = [ind.fitness.values[0] for ind in pop]
    fitness_history += [fits.copy()]

    g = 0
    min_fits, max_fits, avg_fits, var_fits = [], [], [], []
    while min(fits) > target_lambda and g < gens:
        g = g + 1

        elite = tools.selBest(pop, elitism_k)
        offspring = toolbox.select(pop, len(pop) - elitism_k - new_inds_per_gen) + elite
        offspring = list(map(toolbox.clone, offspring)) + toolbox.generate_population(n = new_inds_per_gen)

        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            if random.random() < cxpb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < mutpb:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.parallel_map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]
        fitness_history += [fits.copy()]

        if verbose == 2:
            min_fits += [min(fits)]
            max_fits += [max(fits)]
            avg_fits += [statistics.mean(fits)]
            var_fits += [statistics.variance(fits)]

        if verbose and (g % (gens // 10) == 0 or g == 1):
                print(f'Generation {g}')
                if verbose == 2:
                    print('  Min %s' % min_fits[-1])
                    print('  Max %s' % max_fits[-1])
                    print('  Avg %s' % avg_fits[-1])
                    print('  Var %s' % var_fits[-1])

    timeout = min(fits) == target_lambda

    return {'fitness_history': fitness_history,
            'timeout': timeout}



if __name__ == '__main__':
    # pool = multiprocessing.Pool(processes = 1)

    # 1.
    # Each run returns a dict with the keys:
    #
    # 'fitness_history': A list of sublists. Each sublist contains the fitness values of a generation.
    #                    The first sublist has the fitness values of the initial (random) population.
    #                    The next sublists contain the fitness values at the end of generation 1, 2, 3, etc.
    #
    #  'timeout': Whether the algorithm found a result or timed out.

    # 2.
    # All results from runs for a problem instance (configuration) are placed in a dict with the keys:
    #
    # 'parameters': A tuple containing (V, B, R, TARGET_LAMBDA) for the current configuration.
    # 'times_taken': A list with how long each of the runs took in seconds.
    # 'results': The dicts returned by each of the runs.

    # 3.
    # All results from configurations of the same type (toy, small, medium, etc.) will be placed in a dict mapping a
    # tuple of (V, B, R, TARGET_LAMBDA) to the result dict from 2. that contains data for the runs of that
    # configuration.

    # E.g.
    #
    # final_result['small'][(6, 25, 25, 15)]['times_taken']
    #                ^              ^
    #                |              |
    #         configuration type    |
    #                               |
    #                     (V, B, R, TARGET_LAMBDA)

    results_by_configuration_type = dict()
    for configuration_type, configuration_instances in CONFIGURATIONS.items():
        print(f'Running [{configuration_type}] configurations:')

        configuration_type_results = dict()
        for configuration_instance in configuration_instances:
            v, b, r, target_lambda, elitism_k, new_inds_per_gen = configuration_instance
            print(f'Running configuration: V={v} B={b} R={r} λ={target_lambda}:')

            creator.create('FitnessMin', base.Fitness, weights = (-1.0,))
            creator.create('Individual', list, fitness = creator.FitnessMin)

            toolbox = base.Toolbox()
            toolbox.register('generate_individual_attrs', opd_operators.generate_individual, v = v, b = b, r = r)
            toolbox.register('generate_individual', lambda: creator.Individual(toolbox.generate_individual_attrs()))
            toolbox.register('generate_population', tools.initRepeat, list, toolbox.generate_individual)
            toolbox.register('evaluate', opd_operators.evaluate)
            toolbox.register('mate_gene', opd_operators.gene_cx_sets_uniform_exchange, k = CX_K)
            toolbox.register('mate', opd_operators.cx_1point, cx_gene = toolbox.mate_gene)
            toolbox.register('mutate', opd_operators.mut_relocate_1s, genepb = MUT_GENEPB, k = MUT_K, b = b)
            toolbox.register('select', tools.selTournament, tournsize = 3)

            toolbox.register('parallel_map', lambda *args: list(map(*args)))

            toolbox.register('generate_individual_attrs', opd_operators.generate_individual, v = v, b = b, r = r)
            toolbox.register('generate_individual', lambda: creator.Individual(toolbox.generate_individual_attrs()))
            toolbox.register('generate_population', tools.initRepeat, list, toolbox.generate_individual)

            times_taken_for_configuration = []
            results_for_configuration = []
            for run_ind in range(RUNS_PER_CONFIGURATION):
                print(f'Run {run_ind+1} / {RUNS_PER_CONFIGURATION} for current configuration:')

                start = time.clock()
                # verbose 1/True -> print generation numbers
                # verbose 2 -> print stats for generations
                result = run_opd_ga(toolbox,
                                    popsize = POPSIZE,
                                    gens = GENS,
                                    cxpb = CXPB,
                                    mutpb = MUTPB,
                                    elitism_k = elitism_k,
                                    new_inds_per_gen = new_inds_per_gen,
                                    target_lambda = target_lambda,
                                    verbose = False)
                end = time.clock()

                time_taken = end - start
                times_taken_for_configuration += [time_taken]
                results_for_configuration += [result]

            configuration_instance_results = {'parameters': (v, b, r, target_lambda),
                                              'times_taken': times_taken_for_configuration,
                                              'results': results_for_configuration}

            configuration_type_results[configuration_instance_results['parameters']] = configuration_instance_results

        results_by_configuration_type[configuration_type] = configuration_type_results

    result_file_name = 'ga-results-' + str(datetime.datetime.now()).replace(' ', '-').replace(':', '-').replace('.', '-') + '.pkl'
    print(f'Saving results to {result_file_name}...')

    with open(result_file_name, 'wb') as result_file:
        pickle.dump(results_by_configuration_type, result_file)

    print('Done.')

    # plt.plot(min_fits, marker = 'o', markersize = 5.0, linewidth = 3.0, label = 'Min. Fits')
    # plt.plot(max_fits, marker = 'o', markersize = 5.0, linewidth = 3.0, label = 'Max. Fits')
    # plt.plot(avg_fits, marker = 'o', markersize = 5.0, linewidth = 3.0, label = 'Avg. Fits')
    # plt.title('Fitness (λ) Evolution')
    # plt.ylabel('Fitness (λ)')
    # plt.xlabel('Generation')
    # plt.legend()
    # plt.grid(True)
    # plt.show()
