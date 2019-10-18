from matplotlib import pyplot as plt


mean_time = {1: {14:   0.10,
                 13:   0.11,
                 12:   0.17,
                 11:   0.54,
                 10:   2.10,
                  9:  10.57,
                  8:  56.15,
                  7: 100},

             2: {14:   0.12,
                 13:   0.12,
                 12:   0.13,
                 11:   0.13,
                 10:   0.13,
                  9:   0.15,
                  8:   0.29,
                  7:   1.15,
                  6: 100},

             3: {14:   0.13,
                 13:   0.24,
                 12:   0.26,
                 11:   0.26,
                 10:   0.27,
                  9:   0.29,
                  8:   1.00,
                  7:   1.04,
                  6:  27.59,
                  5: 100},

             4: {14:   0.99,
                 13:   1.00,
                 12:   0.15,
                 11:   0.11,
                 10:   0.09,
                  9:   0.35,
                  8:   0.55,
                  7:   0.58,
                  6:   5.87,
                  5: 100}}

median_time = {1: {14:   0.09,
                   13:   0.09,
                   12:   0.15,
                   11:   0.53,
                   10:   2.06,
                    9:  10.59,
                    8:  59.26,
                    7: 100},

               2: {14:   0.11,
                   13:   0.11,
                   12:   0.12,
                   11:   0.12,
                   10:   0.12,
                    9:   0.13,
                    8:   0.29,
                    7:   1.18,
                    6: 100},

               3: {14:   0.06,
                   13:   0.07,
                   12:   0.07,
                   11:   0.13,
                   10:   0.14,
                    9:   0.14,
                    8:   0.18,
                    7:   0.87,
                    6:  16.37,
                    5: 100},

               4: {14:   0.98,
                   13:   0.94,
                   12:   0.15,
                   11:   0.09,
                   10:   0.08,
                    9:   0.18,
                    8:   0.18,
                    7:   0.44,
                    6:   0.31,
                    5: 100}}

plt.subplots_adjust(hspace = 0.4)

plt.subplot(2, 1, 1)

models = sorted(list(mean_time.keys()))

for model_ind in models:
    model_data = mean_time[model_ind]
    xs, ys = list(zip(*list(model_data.items())))
    xs = [-x for x in xs]
    plt.plot(xs, ys, marker = '.', linewidth = 2.0, label = f'Model {model_ind}')

plt.title('Mean Time')
plt.xlabel('target λ')
plt.ylabel('time (s)')
plt.legend()
plt.grid()
plt.ylim(0, 10)
plt.xticks([-i for i in range(5, 15)], [str(i) for i in range(5, 15)])


plt.subplot(2, 1, 2)

models = sorted(list(median_time.keys()))

for model_ind in models:
    model_data = median_time[model_ind]
    xs, ys = list(zip(*list(model_data.items())))
    xs = [-x for x in xs]
    plt.plot(xs, ys, marker = '.', linewidth = 2.0, label = f'Model {model_ind}')

plt.title('Median Time')
plt.xlabel('target λ')
plt.ylabel('time (s)')
plt.legend()
plt.grid()
plt.ylim(0, 10)
plt.xticks([-i for i in range(5, 15)], [str(i) for i in range(5, 15)])


plt.show()