import pickle

import numpy as np

from matplotlib import pyplot as plt

with open("ga-results-2020-01-09-04-33-20-137164.pkl", 'rb') as pickle_file:
    results = pickle.load(pickle_file)

print(results)
