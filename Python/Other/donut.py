from math import pi, sin, cos, floor, inf
#from time import sleep
#from os import system
import sys


RADIAN = pi / 180
IMAGE_LENGTH = 65
ILUMINATION = '.-~:;=!*#$@'
ILUMINATION_LEVELS = len(ILUMINATION) - 1
HALF_OF_IMAGE_LENGTH = round(IMAGE_LENGTH / 2)


class Shape:
    def __init__(self):
        self.light_vector = (0, -1, 0)

    def get_light_vector(self) -> tuple:
        return self.light_vector

    def rotate_light_vector(self, alpha: float, beta: float, gamma: float) -> None:
        vector = self.light_vector
        vector = self.x_axis_rotation(vector, (sin(alpha * RADIAN), cos(alpha * RADIAN)))
        vector = self.y_axis_rotation(vector, (sin(beta * RADIAN), cos(beta * RADIAN)))
        vector = self.z_axis_rotation(vector, (sin(gamma * RADIAN), cos(gamma * RADIAN)))
        self.light_vector = vector

    def duplication_by_rotation(self, angle: float, num_of_duplications: int, axis: str, axis_coordinates: tuple[float] = (0, 0, 0)) -> list[list[tuple[float]]]:
        new_points = []

        for i in range (num_of_duplications):                                               
            new_angle = (sin(angle * i * RADIAN), cos(angle * i * RADIAN))
            for point in self.points:
                new_x, new_y, new_z = point[0][0] - axis_coordinates[0], point[0][1] - axis_coordinates[1], point[0][2] - axis_coordinates[2]
                if axis == 'x':
                    conv_x, conv_y, conv_z = self.x_axis_rotation((new_x, new_y, new_z), new_angle)
                    new_coordinates = conv_x + axis_coordinates[0], conv_y + axis_coordinates[1], conv_z + axis_coordinates[2]
                    new_vector = self.x_axis_rotation(point[1], new_angle)
                elif axis == 'y':
                    conv_x, conv_y, conv_z = self.y_axis_rotation((new_x, new_y, new_z), new_angle)
                    new_coordinates = conv_x + axis_coordinates[0], conv_y + axis_coordinates[1], conv_z + axis_coordinates[2]
                    new_vector = self.y_axis_rotation(point[1], new_angle)
                elif axis == 'z':
                    conv_x, conv_y, conv_z = self.z_axis_rotation((new_x, new_y, new_z), new_angle)
                    new_coordinates = conv_x + axis_coordinates[0], conv_y + axis_coordinates[1], conv_z + axis_coordinates[2]
                    new_vector = self.z_axis_rotation(point[1], new_angle)
                
                new_points.append([new_coordinates, new_vector]) 
        
        return new_points

    def duplication_by_shift(self, num_of_duplications: int, vector: tuple) -> list:
        new_points = []
        
        for i in range(num_of_duplications + 1):
            change_vector = (vector[0] / num_of_duplications * i, vector[1] / num_of_duplications * i, vector[2] / num_of_duplications * i)

            for point in self.points:
                new_points.append([(point[0][0] + change_vector[0], point[0][1] + change_vector[1], point[0][2] + change_vector[2]), point[1]])
        
        return new_points
    
    def rotation(self, angles) -> list:
        alpha = (sin(angles[0] * RADIAN), cos(angles[0] * RADIAN))
        beta = (sin(angles[1] * RADIAN), cos(angles[1] * RADIAN))
        gamma = (sin(angles[2] * RADIAN), cos(angles[2] * RADIAN))

        for j in range(len(self.points)):
            new_coordinates = self.x_axis_rotation(self.y_axis_rotation(self.z_axis_rotation(self.points[j][0], gamma), beta), alpha)
            new_vector = self.x_axis_rotation(self.y_axis_rotation(self.z_axis_rotation(self.points[j][1], gamma), beta), alpha)
            self.points[j] = [new_coordinates, new_vector]

    def create_projection(self) -> list[list[str]]:
        lvx, lvy, lvz = self.light_vector
        depth = [[-inf for _ in range(IMAGE_LENGTH)] for _ in range (IMAGE_LENGTH)]
        image = [['  ' for _ in range(IMAGE_LENGTH)] for _ in range (IMAGE_LENGTH)]

        for point in self.points:
            x, y, z = floor(point[0][0] + 0.5) + HALF_OF_IMAGE_LENGTH, floor(point[0][1] + 0.5) + HALF_OF_IMAGE_LENGTH, point[0][2]
            nvx, nvy, nvz = point[1]
            if depth[y][x] >= z: continue
            depth[y][x] = z
            image[y][x] = ILUMINATION[floor(max(lvx * nvx + lvy * nvy + lvz * nvz, 0) * ILUMINATION_LEVELS + 0.5)] + ' '
        
        return image
    
    @staticmethod
    def x_axis_rotation(point_coordinates: tuple, angle: tuple) -> tuple[float]:
        x, y, z = point_coordinates

        new_y = y * angle[1] - z * angle[0]
        new_z = y * angle[0] + z * angle[1]
        return x, new_y, new_z
    
    @staticmethod
    def y_axis_rotation(point_coordinates: tuple, angle: tuple) -> tuple[float]:
        x, y, z = point_coordinates

        new_x = z * angle[0] + x * angle[1]
        new_z = z * angle[1] - x * angle[0]
        return new_x, y, new_z
    
    @staticmethod
    def z_axis_rotation(point_coordinates: tuple, angle: tuple) -> tuple[float]:
        x, y, z = point_coordinates

        new_x = x * angle[1] - y * angle[0]
        new_y = x * angle[0] + y * angle[1]
        return new_x, new_y, z


class Torus(Shape):
    def __init__(self, first_radius: int, second_radius: int) -> None:
        super().__init__()
        self.rotate_light_vector(-45, 0, 0)
        self.points = [[(second_radius, first_radius, 0), (0, 1, 0)]]                                       #Stworzenie punktu (w tablicy punktów) na podstawie którego stworzymy torusa. (druga krotka to wektor normalnej punktu)
        self.points = self.duplication_by_rotation(8, 45, 'z', axis_coordinates = (second_radius, 0, 0))    #Obrót punktu wokół przesuniętej osi Z w celu stworzenia okręgu
        self.points = self.duplication_by_rotation(2, 180, 'y')                                             #Obrót okręgu wokół osi Y w celu stworzenia torusa

#NIE DZIAŁA
class SofCW(Shape):
    def __init__(self, diameter: int) -> None:
        super().__init__()
        self.rotate_light_vector(-45, 0, 0)
        self.points = [[(0, -diameter/3, 0), (0, -1, 0)]]
        self.points = self.duplication_by_rotation(2, 15, 'z', axis_coordinates = (0, 2*diameter/3, 0))
        self.points = self.duplication_by_rotation(-30, 2, 'z', axis_coordinates = (0, 2*diameter/3, 0))
        self.points = self.duplication_by_rotation(120, 3, 'z')
        self.points = self.duplication_by_rotation(4, 90, 'y')


def main():
    figure = Torus(5, 15)
    while True:
        figure.rotation((5, -8, 3))
        display(figure.create_projection())

def display(image: list[list[str]]) -> None:
    sys.stdout.write("\x1B[H\x1B[J\n\n\n" + "\n".join("".join(image[i]) for i in range(IMAGE_LENGTH)))
    sys.stdout.flush()


if __name__ == '__main__':
    main()


"""
import cProfile
from pstats import Stats

if __name__ == '__main__':
    with cProfile.Profile() as pr:
        main()

    with open('profiling_stats.txt', 'w') as stream:
        stats = Stats(pr, stream=stream)
        stats.strip_dirs()
        stats.sort_stats('time')
        stats.dump_stats('.prof_stats')
        stats.print_stats()
"""