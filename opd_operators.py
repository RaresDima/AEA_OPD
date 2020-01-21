import random

import numpy as np

from typing import *


Gene = Set[int]
Individual = List[Gene]


def generate_individual(v: int, b: int, r: int) -> Individual:
    """
    Generate an individual.
    The individual is a list of `v` sets of `r` indices of which elements on that
    row are 1's.
    """
    b_range = list(range(b))
    ind = []
    for row in range(v):
        ind += [set(random.sample(b_range, r))]
    return ind


def evaluate(ind: Individual) -> Tuple[int]:
    """
    Computes the maximum dot product between any 2 rows of the individual.
    """
    max_dot_prod = 0
    for i, row1 in enumerate(ind[:-1]):
        for row2 in ind[i+1:]:
            max_dot_prod = max(max_dot_prod, len(row1 & row2))
    return max_dot_prod,


def cx_1point(ind1: Individual, ind2: Individual,
              cx_gene: Callable[[Gene, Gene], Tuple[Gene, Gene]]) -> Tuple[Individual, Individual]:
    """
    Cuts the list of indices in 1 point.
    """
    cx_point = random.randint(0, len(ind1)-1)
    ind1[:cx_point], ind2[:cx_point] = ind2[:cx_point], ind1[:cx_point]
    ind1[cx_point], ind2[cx_point] = cx_gene(ind1[cx_point], ind2[cx_point])
    return ind1, ind2


def cx_2point(ind1: Individual, ind2: Individual,
              cx_gene: Callable[[Gene, Gene], Tuple[Gene, Gene]]) -> Tuple[Individual, Individual]:
    """
    Cuts the list of indices in 2 points.
    """

    cx_point1 = random.randint(0, len(ind1)-2)
    cx_point2 = random.randint(1, len(ind1)-1)

    if cx_point2 < cx_point1:
        cx_point1, cx_point2 = cx_point2, cx_point1

    if cx_point1 == cx_point2:
        cx_point2 += 1

    ind1[cx_point1:cx_point2], ind2[cx_point1:cx_point2] = ind2[cx_point1:cx_point2], ind1[cx_point1:cx_point2]
    ind1[cx_point1], ind2[cx_point1] = cx_gene(ind1[cx_point1], ind2[cx_point1])
    ind1[cx_point2], ind2[cx_point2] = cx_gene(ind1[cx_point2], ind2[cx_point2])

    return ind1, ind2


def cx_uniform(ind1: Individual, ind2: Individual,
               cx_gene: Callable[[Gene, Gene], Tuple[Gene, Gene]]) -> Tuple[Individual, Individual]:
    """
    Randomly performs CX or ignores each gene with a probability.
    """
    for gene1, gene2 in zip(ind1, ind2):
        cx_gene(gene1, gene2)
    return ind1, ind2


def gene_cx_sets_uniform_exchange(set1: Gene, set2: Gene, k: int) -> Tuple[Gene, Gene]:
    """
    Randomly select `k` (or at most `k` if `k` is too large) from the elements
    of each set that the other set does not have and exchange them between the
    sets.
    """

    diff_1_2 = set1 - set2
    diff_2_1 = set2 - set1

    k = min(k, len(diff_1_2))

    selected_from_1 = set(random.sample(list(diff_1_2), k))
    selected_from_2 = set(random.sample(list(diff_2_1), k))

    for elt_set1, elt_set2 in zip(selected_from_1, selected_from_2):
        set1.remove(elt_set1)
        set1.add(elt_set2)
        set2.remove(elt_set2)
        set2.add(elt_set1)

    return set1, set2


def mut_relocate_1s(ind: Individual, genepb: float, k: int, b: int) -> Individual:
    """
    With a probability, each gene may shift `k` existing 1's into other
    positions.
    """
    for gene in ind:
        if random.random() < genepb:
            to_remove = random.sample(gene, k)
            to_add = random.sample(set(range(b)) - gene, k)
            for rem, add in zip(to_remove, to_add):
                gene.remove(rem)
                gene.add(add)
    return ind


def ind_to_np_array(ind: Individual, v: int, b: int) -> np.ndarray:
    """
    Convert an `Individual` to the corresponding Numpy array for printing.
    """
    np_ind = np.zeros(shape = (v, b), dtype = np.byte)
    for np_row, set_row in zip(np_ind, ind):
        np_row[list(set_row)] = 1
    return np_ind


def np_array_to_pretty_np_array(ind: np.ndarray) -> str:
    w = ind.shape[1]
    return \
        '+' + '-' * (2*w + 1) + '+\n| ' + \
        str(ind).replace('[', '').replace(']', '').replace('0', ' ').replace('\n ', ' |\n| ') + ' |\n+' + \
        '-' * (2*w + 1) + '+'


if __name__ == '__main__':

    from functools import partial

    np.set_printoptions(linewidth = 300)

    V, B, R = 10, 37, 14

    pop = generate_population(3, V, B, R)

    print('POP\n--------------')

    for i in range(2):
        print(ind_to_np_array(pop[i], V, B))
        print('--------------')

    print('CX\n--------------')

    cx_1point(pop[0], pop[1], partial(gene_cx_sets_uniform_exchange, k=5))

    for i in range(2):
        print(ind_to_np_array(pop[i], V, B))
        print('--------------')

    print('SET k=3\n--------------')

    print(pop[0][0])
    print(pop[0][1])
    print('--------------')
    gene_cx_sets_uniform_exchange(pop[0][0], pop[0][1], k = 3)
    print(pop[0][0])
    print(pop[0][1])
    print('--------------')












