from math import log2

COLORS       = "🟥🟧🟨🟩🟦🟪"
COLOR_VALUES = ["00", "01", "02", "03", "04", "10", "11", "12", "13", "20", "21", "22", "30", "40"]
COLOR_CODES  = ["⬛⬛⬛⬛", "⬜⬛⬛⬛", "⬜⬜⬛⬛", "⬜⬜⬜⬛", "⬜⬜⬜⬜", "🟥⬛⬛⬛", "🟥⬜⬛⬛",
                "🟥⬜⬜⬛", "🟥⬜⬜⬜", "🟥🟥⬛⬛", "🟥🟥⬜⬛", "🟥🟥⬜⬜", "🟥🟥🟥⬛", "🟥🟥🟥🟥"]


def get_color_combinations():
    with open("color_combinations.txt", "r") as file:
        codes = file.readline().strip().split()[1:]
        color_combinations = [line.strip().split()[1:] for line in file]

    return codes, color_combinations


def find_possible_answers(code, color_combinations, possible_codes, color_val):
    code_ind = possible_codes.index(code)
    val = color_combinations[code_ind]
    lines = [ind for ind, elem in enumerate(val) if elem == color_val]
    new_color_combinations = [[color_combinations[j][i] for j in lines] for i in lines]
    new_possible_codes = [possible_codes[i] for i in lines]

    return new_possible_codes, new_color_combinations


def calculate_expected_information(codes, color_combinations):
    number_of_codes = len(codes)
    max_expected_information = 0

    if number_of_codes == 1: return codes[0]
    for ind, code in enumerate(codes):
        color_codes, expected_information = color_combinations[ind], 0

        for color_val in COLOR_VALUES:
            probability = color_codes.count(color_val) / number_of_codes
            if probability == 0.0: continue
            expected_information +=  -probability * log2(probability)

        if expected_information > max_expected_information:
            max_expected_information = expected_information
            best_code = code
    
    return best_code


def get_color_code_from_user(code):
    color_code = input("| Red:   ") + input("| White: ")
    print("\033[2K\033[1A" * 4)
    print(f"| Code: {code} | Ans: {COLOR_CODES[COLOR_VALUES.index(color_code)]} |")
    return color_code

    

def program(all_codes, all_color_combinations, test_mode = False, code = None):
    possible_codes, color_combinations = all_codes, all_color_combinations
    n = 0

    while possible_codes != []:
        n += 1
        best_code = "1233" if n == 1 else calculate_expected_information(possible_codes, color_combinations)

        if not test_mode: 
            code_as_color = ''.join([COLORS[i-1] for i in map(int, list(best_code))])
            print(f"| Code: {code_as_color} |")

        color_code = all_color_combinations[all_codes.index(best_code)][all_codes.index(code)] if test_mode else get_color_code_from_user(code_as_color)

        if color_code == "40" and not test_mode:
            print("\n|  I won! (^-^)  |\n")
            return n

        possible_codes, color_combinations = find_possible_answers(best_code, color_combinations, possible_codes, color_code)
        
    print("\n| Cheater! d-_-b |\n")
    return 1


def test(all_codes, all_color_combinations):
    sum_of_geuesses, code_nr, number_of_geusses_to_win = 0, 0, [0] * 6

    for code in all_codes:
        number_of_geusses = program(all_codes, all_color_combinations, test_mode = True, code = code)

        number_of_geusses_to_win[number_of_geusses-1] += 1
        sum_of_geuesses += number_of_geusses
        code_nr += 1
        if code_nr == 10: return

        print(f"\033[{str(3)}A| Nr:   {code_nr:>4} | Średnia:        {round(sum_of_geuesses / code_nr, 2):>4} |\n| Dystrybucja: {number_of_geusses_to_win}\n")
    

def main(test_mode = False):
    print("[\033[2J")
    all_codes, all_color_combinations = get_color_combinations()
    program(all_codes, all_color_combinations)


if __name__ == "__main__":
    main()