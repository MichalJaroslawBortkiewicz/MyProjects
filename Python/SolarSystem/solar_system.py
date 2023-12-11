#Importowanie potrzebnych funkcji
import pygame
from math import sin, cos, atan2, log, sqrt, exp


#Tworzenie okna programu
pygame.init()
WIDTH, HEIGHT = 1920, 1080
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System")
FONT = pygame.font.SysFont("arial", 12)

#Kolory
RED = (255, 0, 0)
ORANGE = (255, 125, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (100, 100, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 150)
LIGHT_GREY = (200, 200, 200)
GREY = (100, 100, 100)
DARK_YELLOW = (150, 150, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ASTRONOMICAL_UNIT = 149597870700


class CelestialBody:
    GRAVITATIONAL_CONSTANT = 6.6743e-11
    SCALE = 50 / ASTRONOMICAL_UNIT
    DELTA_T = 3600


    def __init__(self, name, x, y, x_vel, y_vel, mass, radius, color):
        self.x = x
        self.y = y
        self.x_vel = x_vel * 1000
        self.y_vel = y_vel * 1000
        
        self.name = name
        self.mass = mass
        self.color = color
        self.radius = sqrt(log(radius))

        self.trail = []


    def draw_object(self, win, zoom):
        x = self.x * zoom * self.SCALE + WIDTH/2
        y = self.y * zoom * self.SCALE + HEIGHT/2
        for xt, yt in self.trail:
            WINDOW.set_at((round(xt * zoom * self.SCALE + WIDTH/2), round(yt * zoom * self.SCALE + HEIGHT/2)), self.color)
        
        pygame.draw.circle(win, self.color, (x, y), round(self.radius * zoom))
        name_text = FONT.render(self.name, 1, WHITE)
        win.blit(name_text, (x - name_text.get_width()/2, y - name_text.get_height() - self.radius*zoom))
    

    def calculate_acceleration(self, celestial_bodies):
        x_acc = y_acc = 0

        for body in celestial_bodies:
            if self == body: continue
            x_distance = body.x - self.x
            y_distance = body.y - self.y
            theta = atan2(y_distance, x_distance)
            acceleration = self.GRAVITATIONAL_CONSTANT * body.mass / (x_distance**2 + y_distance**2)
            x_acc += cos(theta) * acceleration
            y_acc += sin(theta) * acceleration
        
        return (x_acc, y_acc)
            
    
    def update_variables(self, celestial_bodies):
        x_acc, y_acc = self.calculate_acceleration(celestial_bodies)

        self.x += self.x_vel * self.DELTA_T
        self.y += self.y_vel * self.DELTA_T
        self.x_vel += x_acc * self.DELTA_T
        self.y_vel += y_acc * self.DELTA_T
        
        self.trail.append((self.x, self.y))
        if len(self.trail) > 300: self.trail.pop(0)


def Create_Solar_System():
    sun = CelestialBody("Sun", 0, 0, 0, 0, 1.998e30, 696342, YELLOW)
    mercury = CelestialBody("Mercury", 0.387 * ASTRONOMICAL_UNIT, 0, 0, -46.36, 3.285e23, 2439.7, GREY)
    wenus = CelestialBody("Wenus", -0.723 * ASTRONOMICAL_UNIT, 0, 0, 35.02, 4.8675e24, 6051.8, DARK_YELLOW)
    earth = CelestialBody("Earth", ASTRONOMICAL_UNIT, 0, 0, -29.78, 5.972e24, 6371, BLUE)
    mars = CelestialBody("Mars", -1.523 *ASTRONOMICAL_UNIT, 0, 0, 24.07, 6.4171e23, 3389.5, RED)
    jupiter = CelestialBody("Jupiter", -5.2038 * ASTRONOMICAL_UNIT, 0, 0, 13.07, 1.8982e27, 69911, ORANGE)
    saturn = CelestialBody("Saturn", 9.5826 * ASTRONOMICAL_UNIT, 0, 0, -9.68, 5.6834e26, 58232, LIGHT_GREY)
    uran = CelestialBody("Uran", -19.191 * ASTRONOMICAL_UNIT, 0, 0, 6.8, 8.6810e25, 25362, LIGHT_BLUE)
    neptun = CelestialBody("Neptun", 30.07 * ASTRONOMICAL_UNIT, 0, 0, -5.43, 1.024e26, 24622, DARK_BLUE)

    return [sun, mercury, wenus, earth, mars, jupiter, saturn, uran, neptun]


def main():
    run = True
    zoom = 1
    clock = pygame.time.Clock()
    solar_system = Create_Solar_System()

    while run:
        clock.tick(360)

        for body in solar_system:
            body.update_variables(solar_system)
            body.draw_object(WINDOW, exp(zoom))
        
        pygame.display.update()
        WINDOW.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_PLUS: zoom += 0.1
                if event.key == pygame.K_KP_MINUS: zoom -= 0.1

    pygame.quit()


if __name__ == "__main__":
    main()