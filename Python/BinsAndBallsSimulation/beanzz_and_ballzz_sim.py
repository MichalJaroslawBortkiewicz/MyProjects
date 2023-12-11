from random import randint
from time import perf_counter

from multiprocessing.pool import Pool


SAVE_FILE_NAME = "./simulation_data.txt"


def simulate(n : int) -> tuple[int]:
    beanz = [0] * n

    first_col = 0
    all_with_one_ball = 0
    beanz_with_one_ball = 0
    beanz_with_two_ballz = 0
    empty_beanz = n
    

    i = 0
    while beanz_with_two_ballz < n:
        i += 1
        beanz_ind = randint(0, n - 1)
        no_ballz = beanz[beanz_ind]

        if i > n and no_ballz > 1: continue
        elif no_ballz == 0:
            empty_beanz -= 1
            beanz_with_one_ball += 1
        elif no_ballz == 1:
            beanz_with_two_ballz += 1
            if first_col == 0: first_col = i

        beanz[beanz_ind] += 1
        if i < n: continue
        elif i == n: empty_beanz_after_n = empty_beanz
        if beanz_with_one_ball == n and all_with_one_ball == 0: all_with_one_ball = i
    
    return (n, first_col, empty_beanz_after_n, all_with_one_ball, i, i - all_with_one_ball)


def run_simulations(start : int, end : int, diff : int) -> list[tuple[int]]: 
    t_start = perf_counter()
    
    with Pool() as pool, open(SAVE_FILE_NAME, "w+") as file:
        multiple_results = [[pool.apply_async(simulate, (n,)) for _ in range(50)] for n in range(start, end + 1, diff)]

        sum_percentage = 0

        for ind, results in enumerate(multiple_results):
            nt_start = perf_counter()
            for result in results:
                n, bn, un, cn, dn, dn_cn_diff = result.get()
                file.write(f'{n:8}{bn:8}{un:8}{cn:8}{dn:8}{dn_cn_diff:8}\n')
            
            percentage = (ind + 1) / 50.5
            sum_percentage += percentage
            nt = perf_counter() - nt_start
            print(f"{1000*(ind + 1):8} {percentage:>6.3f}% {sum_percentage:>6.3f}% {nt:8.3f}s {nt/percentage:8.3f}spp")

    time_diff = perf_counter() - t_start
    print(f"Time = {(time_diff // 3600):2}h {((time_diff % 3600) // 60):2}m {(time_diff % 60):5.3f}s")


def main():
    run_simulations(1000, 100000, 1000)

if __name__ == "__main__":
    main()
