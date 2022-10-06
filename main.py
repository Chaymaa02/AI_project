import pygame
import pygame_menu
import random
from pygame.locals import *

# shape parameters
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
# animation parameters
SPEED = 20

pygame.mixer.init()
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("images/player1.png").convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        #resize image
        self.surf = pygame.transform.scale(self.surf, (50, 90))
        self.rect = self.surf.get_rect()
        self.rect.center = SCREEN_WIDTH/2, SCREEN_HEIGHT*0.8
    
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-int(SCREEN_WIDTH/3), 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(int(SCREEN_WIDTH/3), 0)

        # Keep player on the screen
        left_corner = int(SCREEN_WIDTH/2 - SCREEN_WIDTH/3)-self.surf.get_width()/2
        right_corner = int(SCREEN_WIDTH/2 + SCREEN_WIDTH/3)+self.surf.get_width()/2
        if self.rect.left < left_corner:
            self.rect.left = left_corner
        if self.rect.right > right_corner:
            self.rect.right = right_corner

class Enemy(pygame.sprite.Sprite):
    def __init__(self, file):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/6,SCREEN_HEIGHT * 0.1))
        self.speed = SPEED


    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect[1] > SCREEN_HEIGHT : 
            random_number = random.randint(0, 5)
            if random_number % 2 != 0:
                self.rect. center = (random_number * SCREEN_WIDTH/6,
                    SCREEN_HEIGHT * 0.1)
            
def draw_road(screen):
    roadmark_w = int(SCREEN_WIDTH/80)
    road_w = int(SCREEN_WIDTH/1.6)

    # draw road
    pygame.draw.rect(
        screen,
        (50, 50, 50),
        (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    # draw left road marking
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (SCREEN_WIDTH/3 , 0, roadmark_w, SCREEN_HEIGHT))
    # draw right road marking
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (2*SCREEN_WIDTH/3, 0, roadmark_w, SCREEN_HEIGHT))

def game(screen, play):
    pygame.mixer.init()
    pygame.init()

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    #add player and enemies
    player = Player()
    enemy = Enemy("images/car.png")
    enemy2 = Enemy("images/otherCar.png")
    #for collision player-enemy
    enemies = pygame.sprite.Group()
    enemies.add(enemy)
    enemies.add(enemy2)
    #for rendering
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemy)
    #for collision enemy-enemy
    enemies2 = pygame.sprite.Group()
    enemies2.add(enemy)


    # Load and play our background music
    pygame.mixer.music.load("audios/sound.wav")
    pygame.mixer.music.play(loops=-1)

    episode = 0
    counter=0
    running = True
    while running:
        counter += 1
        if enemy.rect.top + 20 == player.rect.top:
                episode += 1
        # increase game difficulty overtime
        if counter == 200 and enemy.speed <100:
            enemy.speed += 5
            enemy2.speed += 5
            counter = 0
            print("level up", enemy.speed)


        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop.
            if event.type == QUIT:
                running = False

        
        pressed_keys = pygame.key.get_pressed()  #type = dictionary

        screen.fill((255, 255, 255))
        draw_road(screen)
        #update sprites position
        player.update(pressed_keys)
        enemy.update()
        enemy2.update()

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, then remove the player and stop the loop
            player.kill()
            running = False

        if not pygame.sprite.spritecollideany(enemy2, enemies2):
            screen.blit(enemy2.surf, enemy2.rect)

        text = font.render('Score: ' + str(5), True, (238, 58, 140)) 
        text1 = font.render('Episode: ' + str(episode), True, (238, 58, 140)) 
        text2 = font.render('Max: ' + str(10), True, (238, 58, 140))
        screen.blit(text, (SCREEN_WIDTH - 120, 15)) 
        screen.blit(text1, (SCREEN_WIDTH - 300, 15)) 
        screen.blit(text2, (SCREEN_WIDTH - 450, 15)) 

        pygame.display.flip()

        # Ensure we maintain a 30 frames per second rate
        clock.tick(9)
        

    # At this point, we're done, so we can stop and quit the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()
    menu0 = pygame_menu.Menu('Game Over', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DEFAULT)
    menu0.add.button('Back to Menu', display_menu, screen)
    menu0.add.button('Quit', pygame_menu.events.EXIT)
    menu0.mainloop(screen)
    pygame.quit()

def display_menu(screen):
    you_play = 0
    ai_play = 1
    ai_learn = 2

    menu = pygame_menu.Menu('Welcome', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DEFAULT)
    menu.add.button('Learn AI play', game, screen, ai_learn)
    menu.add.button('Let AI play', game, screen, ai_play)
    menu.add.button('Play yourself', game, screen, you_play)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

if __name__ == '__main__':
    display_menu(screen)