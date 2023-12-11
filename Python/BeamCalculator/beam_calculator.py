from math import sin, cos, tan, pi
from numpy.linalg import solve
import numpy as np


class OutOfBeamException(Exception):
    pass

class InvalidSupportException(Exception):
    pass

class ImpossibleOperationException(Exception):
    pass


class BeamElement:
    def __init__(self, distance: float):
        self.distance = distance
    
    def get_distance(self):
        return self.distance


class Joint(BeamElement):
    def __init__(self, distance: float):
        super().__init__(distance)


class PhysicalQuantity(BeamElement):
    def __init__(self, distance: float, value: float):
        super().__init__(distance)
        self.value = value
    
    def get_value(self):
        return self.value


class Moment(PhysicalQuantity):
    def __init__(self, distance: float, value: float):
        super().__init__(distance, value)
    
    def calculate_moment(self, distance):
        return -self.value * sign(self.distance - distance)


class Force(PhysicalQuantity):
    def __init__(self, distance: float, value: float, angle: float):
        super().__init__(distance, value)
        self.angle = (90 + angle) * pi / 180

    def get_X_comp(self) -> float:
        return self.value * cos(self.angle)

    def get_Y_comp(self) -> float:
        return self.value * sin(self.angle)
    
    def calculate_moment(self, distance):
        return self.get_Y_comp() * (self.distance - distance)


class Support(BeamElement):
    def __init__(self, distance: float):
        super().__init__(distance)
        self.Rx = None
        self.Ry = None

    
    def get_dist_diff(self, distance):
        return (self.distance - distance)
    
    """
    def set_Ry(self, force: float) -> None:
        self.Ry = force

    def get_Ry(self) -> float:
        return self.Ry
    
    def set_Rx(self, force: float) -> None:
        self.Rx = force

    def get_Rx(self) -> float:
        return self.Rx
    """


class PinnedSupport(Support):
    def __init__(self, distance: float):
        super().__init__(distance)


class RollerSupport(Support):
    def __init__(self, distance: int, angle: float):
        super().__init__(distance)

        if angle <= -90 or angle >= 90: raise InvalidSupportException
        if angle == 0: self.Rx = 0
        self.angle = angle

    """
    def calculate_Rx_from_Ry(self):
        self.Rx = self.Ry * tan(self.angle)
    
    def calculate_Ry_from_Rx(self):
        if self.angle == 0: raise ImpossibleOperationException
        self.Ry = self.Rx / tan(self.angle)
    """


    def get_angle(self) -> float:
        return self.angle


class Beam:
    def __init__(self, length):
        self.continous_loads : list = []
        self.forces : list[Force] = [] 
        self.moments : list[Moment] = []
        self.supports : list[Support] = []

        self.length = length

    def add_force(self, force : Force) -> None:
        self.forces.append(force)
    
    def add_moment(self, moment : Moment) -> None:
        self.moments.append(moment)
    
    def add_support(self, support : Support) -> None:
        self.supports.append(support)
    
    """
    def add_force(self, force : Force) -> None:
        self.forces.append(force)
    """
        

    def solve_beam(self):
        no_supports = len(self.supports)
        variable_matrix = [[1, 0] * no_supports,
                           [0, 1] * no_supports]
        result_matrix = [round(sum(force.get_X_comp() for force in self.forces), 10),
                         round(sum(force.get_Y_comp() for force in self.forces), 10)]

        for ind, support in enumerate(self.supports):
            if type(support) != RollerSupport: continue
            arr = [0] * (2 * no_supports)
            arr[2 * ind] = -1
            arr[2 * ind + 1] = round(1 / tan(pi/2 + support.get_angle()), 15)
            variable_matrix.append(arr)
            result_matrix.append(0)
        
        
        missing_rows = 2 * no_supports - len(variable_matrix)
        for n in range(missing_rows):
            dist = self.length * (n + 1) / (missing_rows + 1) 
            if len(variable_matrix) == 2 * no_supports: break
            arr = []
            for support in self.supports:
                arr += [0, support.get_dist_diff(dist)]
            variable_matrix.append(arr)


            summed_moment = sum(force.calculate_moment(dist) for force in self.forces)
            summed_moment += sum(moment.calculate_moment(dist) for moment in self.moments)

            result_matrix.append(summed_moment)

        print(variable_matrix, result_matrix)
        return self.get_answer(variable_matrix, result_matrix)



    def get_answer(self, variable_matrix, result_matrix):
        for i in solve(np.array(variable_matrix), np.array(result_matrix)):
            print(round(i, 10))

    def show(self):
        print("\n " + "_" * 4 * self.length)
        supports_pos = [support.distance for support in self.supports]
        for i in range(2 * self.length + 1):
            if i / 2 not in supports_pos: print("  ", end="")
            else: print("/\\", end = "")
        print()
    

def sign(x):
    if x == 0: return 0
    return x / abs(x)


def main():
    beam = Beam(16)
    beam.add_force(Force(2, 10, 0))
    beam.add_support(PinnedSupport(0))
    beam.add_support(RollerSupport(10, 0))
    beam.add_moment(Moment(16, 20))
    beam.solve_beam()
    beam.show()


if __name__ == "__main__":
    main()