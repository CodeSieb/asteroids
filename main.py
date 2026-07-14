import pygame
import sys
from logger import log_state, log_event
from constants import *
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from shot import Shot

pygame.init()

clock = pygame.time.Clock()





def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    
    player_score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = (updatable)

    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    asteroidfield = AsteroidField()

    dt = 0.0

    while True:

        my_font = pygame.font.SysFont(None, 30)
        score_text = my_font.render(f"Score: {player_score}", True, "white")
        screen.blit(score_text, (10, 10))





        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                if player.lives < 1:
                    log_event("player_hit")
                    print("Game over!")
                    sys.exit()
                else:
                    log_event("player_hit")
                    player.lives -= 1
                    asteroid.split()
            for ast in asteroids:
                if ast.collides_with(asteroid):
                    ast.reverse_direction()
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    player_score += 1
                    

        
                

        screen.fill("black")
        score_text = my_font.render(f"Score: {player_score}", True, "white")
        lives_text = my_font.render(f"Lives: {player.lives}", True, "white")
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()


