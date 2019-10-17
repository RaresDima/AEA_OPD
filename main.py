import os
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
GECODE_PATH = r'E:\Tools\Gecode\bin\fzn-gecode'
MODEL_PATH  = r'.\models\FinancialPortfolio.mzn'

V, B, R = 10, 37, 14
TARGET_LAMBDA = 9

###################

DATA_PATH = write_datafile(MODEL_PATH, V, B, R, TARGET_LAMBDA)

MODEL_PATH = os.path.abspath(MODEL_PATH)
DATA_PATH = os.path.abspath(DATA_PATH)
FZN_PATH = os.path.abspath(f'{os.path.splitext(MODEL_PATH)[0]}.fzn')
OZN_PATH = os.path.abspath(f'{os.path.splitext(MODEL_PATH)[0]}.ozn')

###################

print(f'SOLVER   : {SOLVER_NAME} \n'
      f'MODEL    : {MODEL_PATH}   \n'
      f'DATA     : {DATA_PATH}\n'
      f'FLATZINC : {FZN_PATH} \n'
      f'OZN PATH : {OZN_PATH} \n'
      f'DATA: V = {V} \n'
      f'      B = {B} \n'
      f'      R = {R} \n'
      f'      LAMBDA <= {TARGET_LAMBDA} \n'
      f'Compiling...')

subprocess.check_call([MINIZINC_PATH, '--compile', '--solver', SOLVER_NAME, MODEL_PATH, DATA_PATH])

print('Done.')

print('Solving...')
solve_output = subprocess.check_output([GECODE_PATH, FZN_PATH]).decode()
print('Done')

solve_result = np.array(solve_output[solve_output.find('[')+1:solve_output.find(']')].strip().split(', ')).reshape((V, B))
print(solve_result)



os.remove(DATA_PATH)
os.remove(FZN_PATH)
os.remove(OZN_PATH)


