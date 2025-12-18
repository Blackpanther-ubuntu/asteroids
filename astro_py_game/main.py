import sys

import pygame

from asteroidfield import AsteroidField
from astroids import Asteroid
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0
    score = 0
    lifes = 2
    color = "white"

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        if lifes == 2:
            color = "green"
        if lifes == 1:
            color = "orange"
        if lifes == 0:
            color = "red"
        updatable.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                if lifes == 0:
                    log_event("player_hit")
                    print("Game over!")
                    print(f"You shot down {score} asteroids")
                    sys.exit()
                else:
                    lifes -= 1
                    asteroid.kill()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split(score)

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen, color)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
