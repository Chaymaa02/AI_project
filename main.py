import pygame
import pygame_menu
import random
from pygame.locals import *
from algoFunctions import *
from algoFunctions2 import *


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
        self.position = 0 #It is on the center
    
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-int(SCREEN_WIDTH/3), 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(int(SCREEN_WIDTH/3), 0)

        #update position     
        if self.rect.center[0] > 2*SCREEN_WIDTH/3 :
            self.position = 1
        elif self.rect.center[0] < SCREEN_WIDTH/3 :
            self.position = 2
        else :
            self.position = 0
            
        # Keep player on the screen
        left_corner = int(SCREEN_WIDTH/2 - SCREEN_WIDTH/3)-self.surf.get_width()/2
        right_corner = int(SCREEN_WIDTH/2 + SCREEN_WIDTH/3)+self.surf.get_width()/2
        if self.rect.left < left_corner:
            self.rect.left = left_corner
        if self.rect.right > right_corner:
            self.rect.right = right_corner
        
    def update_AI(self, action):
        """
        action = 0 : do nothing
        action = 1 : move right
        action = 2 : move left
        """
        if action == 2:
                self.rect.move_ip(-int(SCREEN_WIDTH/3), 0)
        if action == 1:
                self.rect.move_ip(int(SCREEN_WIDTH/3), 0)

        # Keep player on the screen
        left_corner = int(SCREEN_WIDTH/2 - SCREEN_WIDTH/3)-self.surf.get_width()/2
        right_corner = int(SCREEN_WIDTH/2 + SCREEN_WIDTH/3)+self.surf.get_width()/2
        if self.rect.left < left_corner:
            self.rect.left = left_corner
        if self.rect.right > right_corner:
            self.rect.right = right_corner
        
        #update position     
        if self.rect.center[0] > 2*SCREEN_WIDTH/3 :
            self.position = 1
        elif self.rect.center[0] < SCREEN_WIDTH/3 :
            self.position = 2
        else :
            self.position = 0
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, file):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load(file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH/6,SCREEN_HEIGHT * 0.1))
        self.speed = SPEED
        self.position = 2 #the enemy is located on the left


    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect[1] > SCREEN_HEIGHT : 
            random_number = random.randint(0, 5)
            if random_number % 2 != 0:
                self.rect. center = (random_number * SCREEN_WIDTH/6,
                    SCREEN_HEIGHT * 0.1)
                if random_number == 3 :
                    self.position = 0
                elif random_number == 5 :
                    self.position = 1
                else:
                    self.position = 2
            
def draw_road(screen):
    roadmark_w = int(SCREEN_WIDTH/80)
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

def game(screen, max_score, play):
    pygame.mixer.init()
    pygame.init()

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    #add player and enemies
    player = Player()
    enemy = Enemy("images/car.png")
    #for collision player-enemy
    enemies = pygame.sprite.Group()
    enemies.add(enemy)
    #for rendering
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemy)
    if play == 0 or play == 3:
        enemy2 = Enemy("images/otherCar.png")
        enemies.add(enemy2)
        #for collision enemy-enemy
        enemies2 = pygame.sprite.Group()
        enemies2.add(enemy)


    # Load and play our background music
    # pygame.mixer.music.load("audios/sound.wav")
    # pygame.mixer.music.play(loops=-1)

    lr = .89
    dr = .99
    epsilon = 1.0
    points = 0
    score = 0
    episode = 0
    counter=0
    running = True
    while running:
        counter += 1
        if enemy.rect.center[1] == SCREEN_HEIGHT * 0.1:
            if play == 3 : 
                state = State2(player, enemies)
            else:
                state = State(player, enemy)
            episode += 1

        # increase game difficulty overtime
        # if counter == 200 and enemy.speed <100:
        #     enemy.speed += 5
        #     if play ==0:
        #         enemy2.speed += 5
        #     counter = 0
        #     print("level up", enemy.speed)


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
        

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        if play == 0: # You play
            score = episode -1
            #update sprites position
            player.update(pressed_keys)
            enemy.update()
            enemy2.update()

            # Check if any enemies have collided with the player
            if pygame.sprite.spritecollideany(player, enemies):
                # If so, then remove the player and stop the loop
                player.kill()
                running = False 

        if play == 0 or play == 3:
            # Check if car2(enemy2) have collided with the other enemy (car)
            if not pygame.sprite.spritecollideany(enemy2, enemies2):
                #if not, draw it
                screen.blit(enemy2.surf, enemy2.rect)  

        if play == 2 or play ==1 or play == 3 : #AI play
            #update sprites position
            enemy.update()
            if play == 3:
                enemy2.update()

            if play == 1:
                epsilon = 0
            if play == 3:
                action = get_action2(state, epsilon)
                player.update_AI(action) #move to new state=action
                reward = get_reward2(player, enemies)
                points +=reward
                new_state = State2(player, enemies)
                s = state.get_state()
                qTable2[s][action] = qTable2[s][action] + lr *(reward+dr*np.max(qTable2[new_state.get_state()][:])-qTable2[s][action])
                state = new_state
                if reward == -100:
                    score = 0
                    Data.append(points)
                    points = 0
                elif reward == 10:
                    score += 1
                    Data.append(points)
                    points = 0
            else:
                action = get_action(state, epsilon)
                player.update_AI(action) #move to new state=action
                reward = get_reward(player, enemies)
                points +=reward
                new_state = State(player, enemy)
                s = state.get_state()
                if play == 2 :
                    qTable[s][action] = qTable[s][action] + lr *(reward+dr*np.max(qTable[new_state.get_state()][:])-qTable[s][action])
                state = new_state
                if reward == -100:
                    score = 0
                    Data.append(points)
                    points = 0
                elif reward == 2:
                    score += 1
                    Data.append(points)
                    points = 0   
            
            if epsilon > epsilon_min:
                epsilon = epsilon * epsilon_decay

            
        
        text = font.render('Score: ' + str(score), True, (238, 58, 140)) 
        text1 = font.render('Episode: ' + str(episode), True, (238, 58, 140)) 
        text2 = font.render('Max: ' + str(max_score), True, (238, 58, 140))
        screen.blit(text, (SCREEN_WIDTH - 120, 15)) 
        screen.blit(text1, (SCREEN_WIDTH - 300, 15)) 
        screen.blit(text2, (SCREEN_WIDTH - 450, 15)) 

        pygame.display.flip()
        #update the maximum score
        if score >= max_score:
            max_score = score

        # Ensure we maintain a 30 frames per second rate
        clock.tick(9)
            

    f = open('data.txt', 'w')
    f.write(str(Data))
    f.close()

    g = open('qTable.txt', 'w')
    g.write(str(qTable))
    g.close()  

    t = open('qTable3.txt', 'w')
    t.write(str(qTable2))
    t.close() 

    # At this point, we're done, so we can stop and quit the mixer
    # pygame.mixer.music.stop()
    # pygame.mixer.quit()
    menu0 = pygame_menu.Menu('Game Over', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DEFAULT)
    menu0.add.button('Back to Menu', display_menu, screen, max_score)
    menu0.add.button('Quit', pygame_menu.events.EXIT)
    menu0.mainloop(screen)
    pygame.quit()

def display_menu(screen, max_score):
    you_play = 0
    ai_play = 1
    ai_learn = 2
    ai_learn2 = 3

    menu = pygame_menu.Menu('Welcome', width=SCREEN_WIDTH, height=SCREEN_HEIGHT, theme=pygame_menu.themes.THEME_DEFAULT)
    menu.add.button('Let AI learn', game, screen, max_score, ai_learn)
    menu.add.button('Let AI play', game, screen, max_score, ai_play)
    menu.add.button('Let AI learn level 2', game, screen, max_score, ai_learn2)
    menu.add.button('Play yourself', game, screen, max_score, you_play)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    menu.mainloop(screen)

if __name__ == '__main__':
    display_menu(screen, max_score)