from math import sin, cos, pi
from copy import deepcopy
import sys

DELTA_T = 0.0075
RADIAN = pi/180

FRAME_LENGTH = 63
FRAME_HEIGHT = 63

FIRST_ARM_MASS = 10
SECOND_ARM_MASS = 10
MASS_SUM = FIRST_ARM_MASS + SECOND_ARM_MASS

FIRST_ARM_STARTING_ANGLE = 90
SECOND_ARM_STARTING_ANGLE = 179

FIRST_ARM_AIR_RESISTANCE = 0
SECOND_ARM_AIR_RESISTANCE = 0

FIRST_ARM_LENGTH = 15
SECOND_ARM_LENGTH = 15

X_SHIFT = FRAME_LENGTH//2
Y_SHIFT = 24

GRAVITY_CONST = 9.81

DATA = [f"{DELTA_T = }",
        f"{GRAVITY_CONST = }", '',
        f"{FRAME_LENGTH = }",
        f"{FRAME_HEIGHT = }", '',
        f"{FIRST_ARM_MASS  = }",
        f"{SECOND_ARM_MASS = }", '',
        f"{FIRST_ARM_LENGTH  = }",
        f"{SECOND_ARM_LENGTH = }", '',
        f"{FIRST_ARM_STARTING_ANGLE  = }",
        f"{SECOND_ARM_STARTING_ANGLE = }", '',
        f"{FIRST_ARM_AIR_RESISTANCE  = } To jeszcze do poprawy! Na razie nie działa!",
        f"{SECOND_ARM_AIR_RESISTANCE = } To jeszcze do poprawy! Na razie nie działa!"]


def create_frame(): #utworzenie "klatki" na którą rzucamy projekcję wahadła
    frame = [['  ' for _ in range(FRAME_LENGTH)] for _ in range(FRAME_HEIGHT)]
    for i in range(1,FRAME_LENGTH - 1): frame[i][0], frame[i][FRAME_LENGTH - 1] = '| ', ' | '
    for i in range(1,FRAME_HEIGHT - 1): frame[0][i], frame[FRAME_HEIGHT - 1][i] = '__', '__'
    frame[0][0], frame[0][FRAME_LENGTH - 1], frame[FRAME_HEIGHT - 1][0], frame[FRAME_HEIGHT - 1][FRAME_LENGTH - 1] = '__', '__', '|_', '_|'
    return frame


def compute_first_angle_double_dot(first_angle, first_angle_dot, second_angle, second_angle_dot): #wyliczenie wartości przyspieszenia kątowego pierwszego kąta ze wzoru
    angle_difference = first_angle - second_angle
    return  (-SECOND_ARM_MASS * 0.5 * sin(2*angle_difference) * FIRST_ARM_LENGTH * (first_angle_dot**2)
    + SECOND_ARM_MASS * GRAVITY_CONST * cos(angle_difference) * sin(second_angle)
    - SECOND_ARM_MASS * SECOND_ARM_LENGTH * (second_angle_dot**2) * sin(angle_difference) 
    - MASS_SUM * GRAVITY_CONST * sin(first_angle))/(FIRST_ARM_LENGTH * (MASS_SUM - SECOND_ARM_MASS * (cos(angle_difference)**2)))


def compute_second_angle_double_dot(first_angle, first_angle_dot, second_angle, second_angle_dot): #wyliczenie wartości przyspieszenia kątowego drugiego kąta ze wzoru
    angle_difference = first_angle - second_angle
    return  ((MASS_SUM * (FIRST_ARM_LENGTH * (first_angle_dot**2)*sin(angle_difference)
    + GRAVITY_CONST * cos(angle_difference) * sin(first_angle) - GRAVITY_CONST * sin(second_angle))
    + 0.5 * sin(2*angle_difference) * (second_angle_dot**2) * SECOND_ARM_MASS * SECOND_ARM_LENGTH)
    /(SECOND_ARM_LENGTH*(FIRST_ARM_MASS + SECOND_ARM_MASS*(sin(angle_difference)**2))))


def project_pendulum(first_angle, second_angle, first_ang_vel, second_ang_vel, frame_patern):
    frame = deepcopy(frame_patern) #zrobienie kopii ramki
    sofa, cofa, sosa, cosa = sin(first_angle * RADIAN), cos(first_angle * RADIAN), sin(second_angle * RADIAN), cos(second_angle * RADIAN)
    pendulum_data = [f"{first_angle    = }", f"{second_angle   = }", f"{first_ang_vel  = }", f"{second_ang_vel = }"]

    for i in range(FIRST_ARM_LENGTH + 1): frame[round(i*cofa) + Y_SHIFT][round(i*sofa) + X_SHIFT] = 'o '
    for i in range(SECOND_ARM_LENGTH + 1): frame[round(FIRST_ARM_LENGTH*cofa + i*cosa) + Y_SHIFT][round(FIRST_ARM_LENGTH * sofa + i*sosa) + X_SHIFT] = 'o '
    
    joined_frame = ["".join(frame[i]) for i in range(FRAME_HEIGHT)]
    for i,e in enumerate(DATA): joined_frame[i+1] += e 
    for i,e in enumerate(pendulum_data): joined_frame[i+19] += e 
    
    sys.stdout.write("\x1B[J\n\n" + "\n".join(joined_frame))
    sys.stdout.flush()


def main():
    frame = create_frame()
    first_angle = FIRST_ARM_STARTING_ANGLE * RADIAN
    second_angle = SECOND_ARM_STARTING_ANGLE * RADIAN
    first_angle_dot = 0
    second_angle_dot = 0
    while True:
        first_angle += first_angle_dot * DELTA_T #first_angle_dot * DELTA_T * (1 - FIRST_ARM_AIR_RESISTANCE * abs(first_angle_dot))
        second_angle += second_angle_dot * DELTA_T #second_angle_dot * DELTA_T * (1 - FIRST_ARM_AIR_RESISTANCE * abs(second_angle_dot))
        first_angle_dot += compute_first_angle_double_dot(first_angle, first_angle_dot, second_angle, second_angle_dot) * DELTA_T
        second_angle_dot += compute_second_angle_double_dot(first_angle, first_angle_dot, second_angle, second_angle_dot) * DELTA_T
        if first_angle > pi: first_angle -= 2*pi
        if first_angle < -pi: first_angle += 2*pi
        if second_angle > pi: second_angle -= 2*pi
        if second_angle < -pi: second_angle += 2*pi
        project_pendulum(first_angle / RADIAN, second_angle / RADIAN, first_angle_dot / RADIAN, second_angle_dot / RADIAN, frame)



if __name__ == '__main__':
    main()
