import os
import time
import subprocess

import numpy as np

from typing import *


np.set_printoptions(linewidth = 300)


def write_datafile(model_path: str, v: int, b: int, r: int, target_lambda: int) -> str:
    data_path = f'{os.path.splitext(model_path)[0]}.dzn'
    with open(data_path, 'w') as data_file:
        data_file.write(f'v = {v};\n'
                        f'b = {b};\n'
                        f'r = {r};\n'
                        f'targetLambda = {target_lambda};\n')
    return data_path


###### CONFIG #####

MINIZINC_PATH = r'E:\Tools\MiniZinc\minizinc'

SOLVER_NAME = 'Gecode'
SOLVER_PATH = r'E:\Tools\Gecode\bin\fzn-gecode'
SOLVER_THREADS = 6
SOLVER_TIME_LIMIT_S = 100

MODEL_PATH  = r'.\models\FinancialPortfolio-v4.mzn'

V, B, R = 10, 37, 14
TARGET_LAMBDA = 6

RUN_COUNT = 30

# ENVIRONMENT SETUP

DATA_PATH = write_datafile(MODEL_PATH, V, B, R, TARGET_LAMBDA)

MODEL_PATH = os.path.abspath(MODEL_PATH)
DATA_PATH = os.path.abspath(DATA_PATH)
FZN_PATH = os.path.abspath(f'{os.path.splitext(MODEL_PATH)[0]}.fzn')
OZN_PATH = os.path.abspath(f'{os.path.splitext(MODEL_PATH)[0]}.ozn')

# PRINT INSTANCE DATA

print(f'SOLVER    : {SOLVER_NAME} \n'
      f'THREADS   : {SOLVER_THREADS} \n'
      f'TIME LIMIT: {SOLVER_TIME_LIMIT_S} s \n'
      f'\n'
      f'MODEL   : {MODEL_PATH}   \n'
      f'DATA    : {DATA_PATH}\n'
      f'FLATZINC: {FZN_PATH} \n'
      f'OZN PATH: {OZN_PATH} \n'
      f'\n'
      f'DATA: V = {V} \n'
      f'      B = {B} \n'
      f'      R = {R} \n'
      f'      LAMBDA <= {TARGET_LAMBDA} \n')

# MODEL COMPILATION

print('Model compiling...')
subprocess.check_call([MINIZINC_PATH, '--compile', '--solver', SOLVER_NAME, '-O5', MODEL_PATH, DATA_PATH])
print('Model compiled.')

# SOLVING BENCHMARK

print('Solving...')

last_good_output = '=====UNKNOWN====='

times = []
for i in range(RUN_COUNT):

    start = time.clock()
    solve_output = subprocess.check_output([SOLVER_PATH,
                                            '-p', str(SOLVER_THREADS),
                                            '-t', str(SOLVER_TIME_LIMIT_S * 1000),
                                            FZN_PATH]).decode()
    stop = time.clock()

    if 'UNKNOWN' not in solve_output:
        last_good_output = solve_output

    times += [stop - start]

    print(f'Solve {i+1:{len(str(RUN_COUNT))}}: {times[-1]} s')

times = [t for t in times if t < SOLVER_TIME_LIMIT_S]

print('Done')
print('Avg. time  :', np.mean(times), 's')
print('Median time:', np.median(times), 's')

# ENVIRONMENT TEARDOWN

if 'UNKNOWN' not in last_good_output:
    solve_result = (
        np.array(
            list(map(
                int,
                last_good_output[last_good_output.find('[')+1:
                                 last_good_output.find(']')]
                    .strip()
                    .split(', ')
            ))
        ).reshape((V, B)))
else:
    solve_result = last_good_output

print(solve_result)

os.remove(DATA_PATH)
os.remove(FZN_PATH)
os.remove(OZN_PATH)


