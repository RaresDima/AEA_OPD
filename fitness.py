import numpy as np


def _max_row_dotprod2(mat: np.ndarray) -> int:
    maxdot = 0
    for i in range(V-1):
        for j in range(i+1, V):
            ri = mat[i, :]
            rj = mat[j, :]
            dot = ri.dot(rj)
            if dot > maxdot:
                maxdot = dot
    return maxdot


def max_row_dotprod(mat: np.ndarray) -> int:
    return max(mat[i, :].dot(mat[j, :])
               for i in range(V-1)
               for j in range(i+1, V))


if __name__ == '__main__':

    import time

    np.set_printoptions(linewidth = 300)


    V, B, R = 10, 37, 14

    ts, ts2 = [], []
    for _ in range(10_000):
        mat = np.random.randint(0, 2, size = (V, B), dtype = np.byte)

        s = time.clock()
        max_row_dotprod(mat)
        ts += [time.clock()-s]

        s = time.clock()
        _max_row_dotprod2(mat)
        ts2 += [time.clock() - s]

    print(f'Avg.  {np.mean(ts):f} s')
    print(f'Avg2. {np.mean(ts2):f} s')

    print(mat)


