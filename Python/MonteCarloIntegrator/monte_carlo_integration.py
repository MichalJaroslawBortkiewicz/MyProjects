import matplotlib.pyplot as plt

from math import pi, sin, pow, sqrt
from random import uniform
from scipy.integrate import quad

#funkcja show z matplotliba nie zawsze działa, dlatego z niej nie korzystałem (ustawiłem bazowo na false)
#Mimo tego przygotowałem kod, tak aby wyświetlić grafy po zmianie na True, ale nie gwarantuję że to działa
#(nie mogłem sprawdzić czy zadziała, więc tylko zakładam że będzie poprawnie)
SHOW = False
SAVE = True

FUNCS_TO_INT = [
    (lambda x: pow(x, 1/3), 0, 8),
    (sin, 0, pi),
    (lambda x: 4 * x * pow(1 - x, 3), 0, 1)
]


def calculate_derivative(func, x, h):
    return (func(x + h) - func(x)) / h


#Finds M >= sup(f(x))
def find_M(func, a, b, n = 10000):
    max_val = max(0, func(a), func(b))
    x, h = a, 1 / n
    prev_derivative = calculate_derivative(func, x, h/2)
    
    while x + h <= b:
        x += h
        try:
            new_derivative = calculate_derivative(func, x, h)
        except ValueError:
            break

        if prev_derivative < 0 or new_derivative > 0: continue
        if max_val >= (result := func(x - h/2)): continue
        max_val = result
    
    #calculated maximum value + error term
    return max_val * (1 + h) 
    

def integrate(func, a, b, n, m):
    c = sum(True for _ in range(n) if func(uniform(a, b)) >= uniform(0, m))
    return c * (b - a) * m / n


def monte_carlo_int(func, a, b, n, m, k, return_list = True):
    results = [integrate(func, a, b, n, m) for _ in range(k)]
    avg = sum(results) / k

    if return_list: return (avg, results)
    else: return avg


def graph_integral_approx(int_plot, func, a, b, k = 50, start = 50, end = 5050, diff = 50):
    x_avg_vals, y_avg_vals = [], []
    x_sim_vals, y_sim_vals = [], []
    
    m = find_M(func, a, b)
    for n in range(start, end, diff):
        avg, results = monte_carlo_int(func, a, b, n, m, k)
        print(f'{n=}, {avg=}')
        x_avg_vals.append(n)
        y_avg_vals.append(avg)
        x_sim_vals.extend([n] * k)
        y_sim_vals.extend(results)
    
    int_plot.plot([start, end], [quad(func, a, b)[0]] * 2, c = "y")
    int_plot.scatter(x_sim_vals, y_sim_vals, c = "b", s = 4)
    int_plot.scatter(x_avg_vals, y_avg_vals, c = "r", s = 16)
    print()


def make_graphs():
    _, plots = plt.subplots(len(FUNCS_TO_INT), 1, figsize = (20, 30))
    for ind, int_param in enumerate(FUNCS_TO_INT):
        graph_integral_approx(plots[ind], *int_param)

    plt.tight_layout()
    if SHOW: plt.show()
    if SAVE: plt.savefig("graphs.png")


def main():
    make_graphs()

    a, b = 0, 2
    func = lambda x: sqrt(b ** 2 - x ** 2)
    pi_approx = monte_carlo_int(func, a, b, 10000, b, 100, return_list=False)
    print(f'\nNot so good approximation of PI based on function sqrt(4 - x^2).\nPI = {pi_approx}')

        
if __name__ == "__main__":
    main()
