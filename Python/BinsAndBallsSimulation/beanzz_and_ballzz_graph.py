from math import log, sqrt
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


unchanged_x      = lambda x, _: x
x_over_n         = lambda x, n: x / n
x_over_sqrtn     = lambda x, n: x / sqrt(n)
x_over_nlogn     = lambda x, n: x / (n * log(n))
x_over_nloglogn  = lambda x, n: x / (n * log(log(n)))
x_over_n_squared = lambda x, n: x / (n ** 2)


GRAPHS_CONFIG = [
    (0, unchanged_x, r'$B_n$'),
    (0, x_over_sqrtn, r'$\frac{B_n}{\sqrt{n}}$'),
    (0, x_over_n, r'$\frac{B_n}{n}$'),
    (1, unchanged_x, r'$U_n$'),
    (1, x_over_n, r'$\frac{U_n}{n}$'),
    (2, unchanged_x, r'$C_n$'),
    (2, x_over_n, r'$\frac{C_n}{n}$'),
    (2, x_over_nlogn, r'$\frac{C_n}{nln(n)}$'),
    (2, x_over_n_squared, r'$\frac{C_n}{n^2}$'),
    (3, unchanged_x, r'$D_n$'),
    (3, x_over_n, r'$\frac{D_n}{n}$'),
    (3, x_over_nlogn, r'$\frac{D_n}{nln(n)}$'),
    (3, x_over_n_squared, r'$\frac{D_n}{n^2}$'),
    (4, unchanged_x, r'$D_n - C_n$'),
    (4, x_over_n, r'$\frac{D_n - C_n}{n}$'),
    (4, x_over_nlogn, r'$\frac{D_n - C_n}{nln(n)}$'),
    (4, x_over_nloglogn, r'$\frac{D_n - C_n}{nln(ln(n))}$'),
]


def linear(x, a, b):
    return a * x + b


"""
def apply_func(data, func):
    return [(x, func(y)) for (x, y) in data]
"""

def apply_func(data, avgs_data, func):
    return ([(n, func(y, n)) for (n, y) in data],
            [(n, func(y, n)) for (n, y) in avgs_data])


def make_graph(data, avgs, graph, title):
    x_data, y_data = np.array(list(zip(*data)))
    x_avg_data, y_avg_data = np.array(list(zip(*avgs)))

    polyline = np.linspace(0, 100000, 101)
    model1 = np.poly1d(np.polyfit(x_data, y_data, 1))
    graph.plot(polyline, model1(polyline), color='green', lw = 3)

    log_curve = np.polyfit(np.log(x_data), y_data, 1)
    graph.plot(x_data, log_curve[0] * np.log(x_data) + log_curve[1], color='orange', lw = 3)

    graph.set_title(title)
    graph.title.set_size(40)
    graph.tick_params(axis='both', which='major', labelsize=20)
    graph.scatter(x_data, y_data, c = "b", s = 4)
    graph.scatter(x_avg_data, y_avg_data, c = "r", s = 24)


def make_graphs(data, avgs):
    _, plots = plt.subplots(4, 2, figsize = (40, 60))
    

    for ind, (data_ind, func, title) in enumerate(GRAPHS_CONFIG):
        if ind < 8:
            make_graph(*apply_func(data[data_ind], avgs[data_ind], func), plots[ind // 2, ind % 2], title)
            continue

        if ind == 8:
            plt.tight_layout()
            plt.savefig("graphs1.png")
            _, plots = plt.subplots(5, 2, figsize = (30, 50))

        make_graph(*apply_func(data[data_ind], avgs[data_ind], func), plots[(ind - 8) // 2, (ind - 8) % 2], title)

    plt.tight_layout()
    plt.savefig("graphs2.png")



def calc_avg(data):
    zipped_data = [(data[50 * i][0], tuple(zip(*[data[i*50 + k][1:] for k in range(50)]))) for i in range(100)]
    avgs_data = tuple(zip(*(tuple(zip([elem[0]] * 5, map(lambda x: sum(x)/50, elem[1]))) for elem in zipped_data)))

    return(avgs_data)


def main():
    with open("./simulation_data.txt", "r+") as file:
        data = [tuple(map(int, file.readline().strip().split())) for _ in range(5000)]

    conv_data = tuple(zip(*(tuple(zip(5 * [n], val)) for n, *val in data)))
    avgs_data = calc_avg(data)

    make_graphs(conv_data, avgs_data) 



if __name__ == "__main__":
    main()