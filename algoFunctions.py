import random
import numpy as np
import pygame

# shape parameters
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
# animation parameters
SPEED = 20
#score parameter
max_score = 0

epsilon_min = 0.001
epsilon_decay = 0.9

Data = []
QTable = np.zeros([6,3])

def get_action(state, epsilon):
    if random.uniform(0, 1) < epsilon:
        action = random.randrange(3)
    else:
        action = np.argmax(QTable[state.get_state(), :])
    return action


def get_reward(player, enemies):
    #Collision between the player and enemy
    if pygame.sprite.spritecollideany(player, enemies):
        return -100
    else :
        for enemy in enemies :
            #if the player is under the enemy
            if enemy.position == player.position :
                return -1
            #if the player skipped the enemy(car)
            elif enemy.rect.center[1] == SCREEN_HEIGHT * 0.9:##############Bug
                return 2
            else :
                return 1 
   
class State:
    def __init__(self, player, enemy):
        self.p = player.position 
        self.e = enemy.position

    def get_state(self):
        res = self.p + self.e
        if res ==8 :
            return 4
        return res