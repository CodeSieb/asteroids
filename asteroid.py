import pygame
import random
from constants import *
from circleshape import CircleShape
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.reverse_direction_cooldown = 0.0

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)
    
    def update(self, dt):
        self.position += (self.velocity * dt)
        self.reverse_direction_cooldown -= dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            random_angle = random.uniform(20, 50)
            self.velocity = self.velocity.rotate(random_angle)
            self.velocity = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid.velocity = self.velocity.rotate(random_angle) * 1.2
            new_asteroid2.velocity = self.velocity.rotate(-random_angle) * 1.2

    def reverse_direction(self):
        if self.reverse_direction_cooldown > 0:
            return
        else: 
            possible_direction = [(110, 160), (-110, -160)]
            direction = random.choice(possible_direction)
            self.velocity = self.velocity.rotate(random.uniform(direction[0], direction[1]))
            self.reverse_direction_cooldown = 1.0